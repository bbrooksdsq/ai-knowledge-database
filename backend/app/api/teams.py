from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from datetime import datetime

from ..core.database import get_db
from ..models.document import Document, DocumentEmbedding
from ..schemas.document import Document as DocumentSchema
from ..services.teams_service import teams_service
from ..services.ai_service import ai_service
from ..api.documents import process_document_ai

router = APIRouter()

@router.post("/sync")
async def sync_teams_recordings(
    days_back: int = 7,
    background_tasks: BackgroundTasks = None
):
    """Sync Teams recordings from the last N days"""
    try:
        # Check if Teams is configured
        if not all([
            teams_service.client_id,
            teams_service.client_secret, 
            teams_service.tenant_id
        ]):
            return {
                "status": "error",
                "message": "Microsoft Teams integration not configured. Please set TEAMS_CLIENT_ID, TEAMS_CLIENT_SECRET, and TEAMS_TENANT_ID environment variables."
            }
        
        # Sync recordings
        processed_documents = await teams_service.sync_teams_recordings(days_back)
        
        return {
            "status": "success",
            "message": f"Successfully synced {len(processed_documents)} Teams recordings",
            "recordings_found": len(processed_documents),
            "documents": processed_documents
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to sync Teams recordings: {str(e)}"
        }

@router.post("/sync-and-store")
async def sync_and_store_teams_recordings(
    days_back: int = 7,
    db: Session = Depends(get_db)
):
    """Sync Teams recordings and store them in the database"""
    try:
        # Check if Teams is configured
        if not all([
            teams_service.client_id,
            teams_service.client_secret, 
            teams_service.tenant_id
        ]):
            raise HTTPException(
                status_code=400, 
                detail="Microsoft Teams integration not configured. Please set TEAMS_CLIENT_ID, TEAMS_CLIENT_SECRET, and TEAMS_TENANT_ID environment variables."
            )
        
        # Sync recordings
        processed_documents = await teams_service.sync_teams_recordings(days_back)
        stored_documents = []
        
        # Store each document in the database
        for doc_data in processed_documents:
            try:
                # Create document
                document = Document(
                    title=doc_data['title'],
                    content=doc_data['content'],
                    file_type=doc_data['file_type'],
                    source=doc_data['source'],
                    file_path=doc_data['file_path'],
                    file_size=doc_data['file_size'],
                    tags=doc_data.get('metadata', {}).get('speakers', []),  # Use speakers as tags
                    entities=doc_data.get('metadata', {}),  # Store all metadata as entities
                    summary=doc_data.get('metadata', {}).get('meeting_summary', '')
                )
                
                db.add(document)
                db.flush()  # Get the ID
                
                # Process with AI (generate embeddings, etc.)
                await process_document_ai(db, document)
                
                db.commit()
                db.refresh(document)
                
                stored_documents.append(document)
                
            except Exception as e:
                db.rollback()
                print(f"Failed to store document {doc_data['title']}: {e}")
                continue
        
        return {
            "status": "success",
            "message": f"Successfully stored {len(stored_documents)} Teams recordings",
            "stored_count": len(stored_documents),
            "documents": [
                {
                    "id": doc.id,
                    "title": doc.title,
                    "created_at": doc.created_at.isoformat(),
                    "summary": doc.summary
                } for doc in stored_documents
            ]
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to sync and store Teams recordings: {str(e)}")

@router.get("/status")
async def get_teams_status():
    """Get Microsoft Teams integration status"""
    try:
        is_configured = all([
            teams_service.client_id,
            teams_service.client_secret, 
            teams_service.tenant_id
        ])
        
        if not is_configured:
            return {
                "configured": False,
                "message": "Microsoft Teams integration not configured",
                "required_variables": [
                    "TEAMS_CLIENT_ID",
                    "TEAMS_CLIENT_SECRET", 
                    "TEAMS_TENANT_ID"
                ]
            }
        
        # Test authentication
        try:
            access_token = await teams_service.get_access_token()
            return {
                "configured": True,
                "authenticated": True,
                "message": "Microsoft Teams integration is ready",
                "tenant_id": teams_service.tenant_id
            }
        except Exception as e:
            return {
                "configured": True,
                "authenticated": False,
                "message": f"Configuration error: {str(e)}"
            }
            
    except Exception as e:
        return {
            "configured": False,
            "authenticated": False,
            "message": f"Error checking status: {str(e)}"
        }

@router.get("/test-connection")
async def test_teams_connection():
    """Test Microsoft Graph API connection"""
    try:
        if not all([
            teams_service.client_id,
            teams_service.client_secret, 
            teams_service.tenant_id
        ]):
            return {
                "status": "error",
                "message": "Microsoft Teams integration not configured"
            }
        
        # Test getting access token
        access_token = await teams_service.get_access_token()
        
        # Test basic Graph API call
        import httpx
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://graph.microsoft.com/v1.0/me",
                headers=headers
            )
            
            if response.status_code == 200:
                return {
                    "status": "success",
                    "message": "Microsoft Graph API connection successful",
                    "authenticated": True
                }
            else:
                return {
                    "status": "error",
                    "message": f"Graph API test failed: {response.status_code} - {response.text}",
                    "authenticated": False
                }
                
    except Exception as e:
        return {
            "status": "error",
            "message": f"Connection test failed: {str(e)}",
            "authenticated": False
        }
