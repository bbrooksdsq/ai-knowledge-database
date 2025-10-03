import httpx
import asyncio
import aiofiles
import os
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import logging
from ..core.config import settings

logger = logging.getLogger(__name__)

class TeamsService:
    def __init__(self):
        self.client_id = settings.TEAMS_CLIENT_ID if hasattr(settings, 'TEAMS_CLIENT_ID') else None
        self.client_secret = settings.TEAMS_CLIENT_SECRET if hasattr(settings, 'TEAMS_CLIENT_SECRET') else None
        self.tenant_id = settings.TEAMS_TENANT_ID if hasattr(settings, 'TEAMS_TENANT_ID') else None
        self.access_token = None
        self.token_expires_at = None
        
    async def get_access_token(self) -> str:
        """Get Microsoft Graph API access token"""
        if self.access_token and self.token_expires_at and datetime.now() < self.token_expires_at:
            return self.access_token
            
        if not all([self.client_id, self.client_secret, self.tenant_id]):
            raise Exception("Microsoft Teams credentials not configured")
        
        token_url = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token"
        
        async with httpx.AsyncClient() as client:
            response = await client.post(token_url, data={
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'scope': 'https://graph.microsoft.com/.default',
                'grant_type': 'client_credentials'
            })
            
            if response.status_code != 200:
                raise Exception(f"Failed to get access token: {response.text}")
            
            token_data = response.json()
            self.access_token = token_data['access_token']
            expires_in = token_data.get('expires_in', 3600)
            self.token_expires_at = datetime.now() + timedelta(seconds=expires_in - 300)  # 5 min buffer
            
            return self.access_token
    
    async def get_teams_recordings(self, days_back: int = 7) -> List[Dict[str, Any]]:
        """Get Teams call recordings from the last N days"""
        try:
            access_token = await self.get_access_token()
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            
            # Calculate date range
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days_back)
            
            # Microsoft Graph API endpoint for call records
            url = f"https://graph.microsoft.com/v1.0/communications/callRecords"
            params = {
                '$filter': f"startDateTime ge {start_date.isoformat()}Z and startDateTime le {end_date.isoformat()}Z",
                '$orderby': 'startDateTime desc'
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers, params=params)
                
                if response.status_code != 200:
                    logger.error(f"Failed to get call records: {response.text}")
                    return []
                
                data = response.json()
                recordings = []
                
                for record in data.get('value', []):
                    # Check if this call has recordings
                    if record.get('type') == 'groupCall' and record.get('callType') in ['group', 'peerToPeer']:
                        # Get recording info if available
                        recording_info = await self.get_recording_info(record['id'], access_token)
                        if recording_info:
                            recordings.append({
                                'id': record['id'],
                                'start_time': record.get('startDateTime'),
                                'end_time': record.get('endDateTime'),
                                'participants': record.get('participants', []),
                                'recording_url': recording_info.get('contentDownloadUrl'),
                                'recording_name': f"Teams Call - {datetime.fromisoformat(record.get('startDateTime', '').replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M')}"
                            })
                
                logger.info(f"Found {len(recordings)} Teams recordings")
                return recordings
                
        except Exception as e:
            logger.error(f"Error getting Teams recordings: {e}")
            return []
    
    async def get_recording_info(self, call_id: str, access_token: str) -> Optional[Dict[str, Any]]:
        """Get recording information for a specific call"""
        try:
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            
            # Try to get recording content
            url = f"https://graph.microsoft.com/v1.0/communications/callRecords/{call_id}/sessions"
            
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers)
                
                if response.status_code == 200:
                    sessions = response.json().get('value', [])
                    for session in sessions:
                        # Check for recording segments
                        segments_url = f"https://graph.microsoft.com/v1.0/communications/callRecords/{call_id}/sessions/{session['id']}/segments"
                        segments_response = await client.get(segments_url, headers=headers)
                        
                        if segments_response.status_code == 200:
                            segments = segments_response.json().get('value', [])
                            for segment in segments:
                                if segment.get('media') and segment['media'].get('recording'):
                                    return {
                                        'contentDownloadUrl': segment['media']['recording'].get('contentDownloadUrl'),
                                        'recordingContentType': segment['media']['recording'].get('recordingContentType')
                                    }
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting recording info for call {call_id}: {e}")
            return None
    
    async def download_recording(self, recording_url: str, filename: str) -> str:
        """Download a Teams recording to local storage"""
        try:
            access_token = await self.get_access_token()
            headers = {
                'Authorization': f'Bearer {access_token}'
            }
            
            # Ensure uploads directory exists
            import os
            os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
            file_path = os.path.join(settings.UPLOAD_DIR, filename)
            
            async with httpx.AsyncClient() as client:
                async with client.stream('GET', recording_url, headers=headers) as response:
                    if response.status_code == 200:
                        async with aiofiles.open(file_path, 'wb') as f:
                            async for chunk in response.aiter_bytes():
                                await f.write(chunk)
                        
                        logger.info(f"Downloaded recording to {file_path}")
                        return file_path
                    else:
                        raise Exception(f"Failed to download recording: {response.status_code}")
                        
        except Exception as e:
            logger.error(f"Error downloading recording: {e}")
            raise
    
    async def process_teams_recording(self, recording_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Process a Teams recording: download, transcribe, and return document data"""
        try:
            if not recording_data.get('recording_url'):
                logger.warning("No recording URL available")
                return None
            
            # Download the recording
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"teams_recording_{timestamp}.mp4"
            file_path = await self.download_recording(recording_data['recording_url'], filename)
            
            # Import AI service for transcription
            from .ai_service import ai_service
            
            # Transcribe the audio
            transcription_result = await ai_service.transcribe_audio_with_speakers(file_path)
            
            # Create document data
            document_data = {
                'title': recording_data['recording_name'],
                'content': transcription_result.get('transcript', ''),
                'file_type': 'teams_recording',
                'source': 'microsoft_teams',
                'file_path': file_path,
                'file_size': os.path.getsize(file_path) if os.path.exists(file_path) else 0,
                'metadata': {
                    'teams_call_id': recording_data['id'],
                    'start_time': recording_data['start_time'],
                    'end_time': recording_data['end_time'],
                    'participants': recording_data['participants'],
                    'speakers': transcription_result.get('speakers', []),
                    'meeting_summary': transcription_result.get('summary', '')
                }
            }
            
            return document_data
            
        except Exception as e:
            logger.error(f"Error processing Teams recording: {e}")
            return None
    
    async def sync_teams_recordings(self, days_back: int = 7) -> List[Dict[str, Any]]:
        """Sync all Teams recordings from the last N days"""
        logger.info(f"Syncing Teams recordings from last {days_back} days")
        
        recordings = await self.get_teams_recordings(days_back)
        processed_documents = []
        
        for recording in recordings:
            try:
                document_data = await self.process_teams_recording(recording)
                if document_data:
                    processed_documents.append(document_data)
                    
                # Add delay between processing to avoid rate limits
                await asyncio.sleep(2)
                
            except Exception as e:
                logger.error(f"Failed to process recording {recording['id']}: {e}")
                continue
        
        logger.info(f"Successfully processed {len(processed_documents)} Teams recordings")
        return processed_documents


# Global instance
teams_service = TeamsService()
