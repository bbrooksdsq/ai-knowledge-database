from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import aiofiles
from datetime import datetime

from ..core.database import get_db
from ..models.document import Document, DocumentEmbedding
from ..schemas.document import Document as DocumentSchema, DocumentCreate, DocumentUpdate, SearchResult, SearchResponse, DocumentSearch
from ..services.ai_service import ai_service
from ..services.search_service import search_service
from ..core.config import settings

router = APIRouter()

@router.post("/", response_model=DocumentSchema)
async def create_document(
    title: str = Form(...),
    content: str = Form(...),
    file_type: str = Form(...),
    source: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    """Create a new document"""
    try:
        file_path = None
        file_size = None
        
        # Handle file upload if provided
        if file:
            # Create uploads directory if it doesn't exist
            os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
            
            # Generate unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{timestamp}_{file.filename}"
            file_path = os.path.join(settings.UPLOAD_DIR, filename)
            
            # Save file
            async with aiofiles.open(file_path, 'wb') as f:
                content_bytes = await file.read()
                await f.write(content_bytes)
                file_size = len(content_bytes)
        
        # Create document
        document = Document(
            title=title,
            content=content,
            file_type=file_type,
            source=source,
            file_path=file_path,
            file_size=file_size
        )
        
        db.add(document)
        db.flush()  # Get the ID
        
        # Process with AI
        await process_document_ai(db, document)
        
        db.commit()
        db.refresh(document)
        
        return document
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create document: {str(e)}")

@router.get("/", response_model=List[DocumentSchema])
async def get_documents(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all documents with pagination"""
    documents = db.query(Document).offset(skip).limit(limit).all()
    return documents

@router.get("/{document_id}", response_model=DocumentSchema)
async def get_document(
    document_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific document by ID"""
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document

@router.put("/{document_id}", response_model=DocumentSchema)
async def update_document(
    document_id: int,
    document_update: DocumentUpdate,
    db: Session = Depends(get_db)
):
    """Update a document"""
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Update fields
    for field, value in document_update.dict(exclude_unset=True).items():
        setattr(document, field, value)
    
    # Reprocess with AI if content changed
    if document_update.content:
        await process_document_ai(db, document)
    
    db.commit()
    db.refresh(document)
    return document

@router.delete("/{document_id}")
async def delete_document(
    document_id: int,
    db: Session = Depends(get_db)
):
    """Delete a document"""
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Delete file if it exists
    if document.file_path and os.path.exists(document.file_path):
        os.remove(document.file_path)
    
    db.delete(document)
    db.commit()
    
    return {"message": "Document deleted successfully"}

@router.post("/search", response_model=SearchResponse)
async def search_documents(
    search_request: DocumentSearch,
    user_id: int = 1,  # In a real app, get from JWT token
    db: Session = Depends(get_db)
):
    """Search documents using semantic search"""
    return await search_service.semantic_search(
        db=db,
        query=search_request.query,
        user_id=user_id,
        limit=search_request.limit,
        filters=search_request.filters
    )

@router.post("/search/keyword", response_model=SearchResponse)
async def search_documents_keyword(
    search_request: DocumentSearch,
    user_id: int = 1,  # In a real app, get from JWT token
    db: Session = Depends(get_db)
):
    """Search documents using keyword search"""
    return await search_service.keyword_search(
        db=db,
        query=search_request.query,
        user_id=user_id,
        limit=search_request.limit,
        filters=search_request.filters
    )

@router.get("/{document_id}/related", response_model=List[DocumentSchema])
async def get_related_documents(
    document_id: int,
    limit: int = 5,
    db: Session = Depends(get_db)
):
    """Get documents related to a specific document"""
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    related_docs = await search_service.get_related_documents(db, document_id, limit)
    return related_docs

async def process_document_ai(db: Session, document: Document):
    """Process document with AI to generate embeddings, tags, etc."""
    try:
        # Generate summary
        summary = await ai_service.generate_summary(document.content)
        document.summary = summary
        
        # Extract tags
        tags = await ai_service.extract_tags(document.content)
        document.tags = tags
        
        # Extract entities
        entities = await ai_service.extract_entities(document.content)
        document.entities = entities
        
        # Generate embeddings for chunks
        chunk_size = 1000  # Characters per chunk
        chunks = [document.content[i:i+chunk_size] for i in range(0, len(document.content), chunk_size)]
        
        for i, chunk in enumerate(chunks):
            embedding = await ai_service.generate_embedding(chunk)
            
            doc_embedding = DocumentEmbedding(
                document_id=document.id,
                embedding=embedding,
                chunk_index=i,
                chunk_text=chunk
            )
            db.add(doc_embedding)
        
        db.flush()
        
    except Exception as e:
        # Log error but don't fail the document creation
        print(f"AI processing failed for document {document.id}: {e}")
