from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


class DocumentBase(BaseModel):
    title: str
    content: str
    file_type: str
    source: Optional[str] = None
    tags: Optional[List[str]] = None
    entities: Optional[Dict[str, Any]] = None
    summary: Optional[str] = None


class DocumentCreate(DocumentBase):
    file_path: Optional[str] = None
    file_size: Optional[int] = None


class DocumentUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[List[str]] = None
    summary: Optional[str] = None


class Document(DocumentBase):
    id: int
    file_path: Optional[str]
    file_size: Optional[int]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class DocumentSearch(BaseModel):
    query: str
    limit: Optional[int] = 10
    filters: Optional[Dict[str, Any]] = None


class SearchResult(BaseModel):
    document: Document
    score: float
    snippet: str


class SearchResponse(BaseModel):
    query: str
    results: List[SearchResult]
    total_results: int
    execution_time: float


class CommentBase(BaseModel):
    content: str


class CommentCreate(CommentBase):
    document_id: int


class Comment(CommentBase):
    id: int
    document_id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
