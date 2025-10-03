from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional
import os
import aiofiles
from datetime import datetime

from ..core.database import get_db
from ..models.document import Document, DocumentEmbedding
from ..schemas.document import Document as DocumentSchema
from ..services.ai_service import ai_service
from ..api.documents import process_document_ai
from ..core.config import settings

router = APIRouter()

@router.post("/audio", response_model=DocumentSchema)
async def transcribe_and_store_audio(
    file: UploadFile = File(...),
    title: Optional[str] = Form(None),
    source: Optional[str] = Form("audio_upload"),
    with_speakers: bool = Form(False),
    db: Session = Depends(get_db)
):
    """Transcribe audio file and store as document"""
    try:
        # Validate file type
        if not file.content_type or not file.content_type.startswith('audio/'):
            raise HTTPException(status_code=400, detail="File must be an audio file")
        
        # Create uploads directory if it doesn't exist
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
        
        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_extension = os.path.splitext(file.filename)[1] if file.filename else '.wav'
        filename = f"audio_{timestamp}{file_extension}"
        file_path = os.path.join(settings.UPLOAD_DIR, filename)
        
        # Save audio file
        async with aiofiles.open(file_path, 'wb') as f:
            content_bytes = await file.read()
            await f.write(content_bytes)
            file_size = len(content_bytes)
        
        # Transcribe audio
        if with_speakers:
            transcription_result = await ai_service.transcribe_audio_with_speakers(file_path)
            transcript_text = transcription_result.get('transcript', '')
            speakers = transcription_result.get('speakers', [])
            meeting_summary = transcription_result.get('summary', '')
            
            # Create enhanced content with speaker info
            content = f"Meeting Transcript\n\n"
            if speakers:
                content += f"Speakers: {', '.join(speakers)}\n\n"
            content += f"Transcript:\n{transcript_text}\n\n"
            if meeting_summary:
                content += f"Summary: {meeting_summary}"
        else:
            transcript_text = await ai_service.transcribe_audio(file_path)
            content = transcript_text
        
        # Generate title if not provided
        if not title:
            title = f"Audio Transcript - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        
        # Create document
        document = Document(
            title=title,
            content=content,
            file_type="audio_transcript",
            source=source,
            file_path=file_path,
            file_size=file_size
        )
        
        db.add(document)
        db.flush()  # Get the ID
        
        # Process with AI (generate embeddings, tags, etc.)
        await process_document_ai(db, document)
        
        db.commit()
        db.refresh(document)
        
        return document
        
    except Exception as e:
        db.rollback()
        # Clean up file if it was created
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")

@router.post("/test-audio")
async def test_audio_transcription():
    """Test endpoint to verify Whisper API connectivity"""
    try:
        if not settings.OPENAI_API_KEY:
            return {
                "status": "error",
                "message": "OpenAI API key not configured",
                "whisper_available": False
            }
        
        # Create a simple test audio file (silence)
        import tempfile
        import wave
        import struct
        
        # Generate 1 second of silence
        sample_rate = 16000
        duration = 1
        samples = [0] * int(sample_rate * duration)
        
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
            with wave.open(temp_file.name, 'w') as wav_file:
                wav_file.setnchannels(1)  # Mono
                wav_file.setsampwidth(2)  # 16-bit
                wav_file.setframerate(sample_rate)
                
                # Write silence
                for sample in samples:
                    wav_file.writeframes(struct.pack('<h', int(sample)))
            
            # Try to transcribe (should return empty or minimal text)
            try:
                transcript = await ai_service.transcribe_audio(temp_file.name)
                os.unlink(temp_file.name)  # Clean up
                
                return {
                    "status": "success",
                    "message": "Whisper API is working",
                    "whisper_available": True,
                    "test_transcript": transcript[:100] if transcript else "Empty audio (expected)"
                }
            except Exception as e:
                os.unlink(temp_file.name)  # Clean up
                return {
                    "status": "error",
                    "message": f"Whisper API test failed: {str(e)}",
                    "whisper_available": False
                }
                
    except Exception as e:
        return {
            "status": "error",
            "message": f"Test setup failed: {str(e)}",
            "whisper_available": False
        }
