from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base


class Document(Base):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    content = Column(Text, nullable=False)
    file_path = Column(String, nullable=True)
    file_type = Column(String, nullable=False)  # pdf, docx, txt, audio, video, etc.
    file_size = Column(Integer, nullable=True)
    
    # Metadata
    source = Column(String, nullable=True)  # upload, email, slack, zoom, etc.
    tags = Column(JSON, nullable=True)  # AI-generated tags
    entities = Column(JSON, nullable=True)  # Extracted entities
    summary = Column(Text, nullable=True)  # AI-generated summary
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    embeddings = relationship("DocumentEmbedding", back_populates="document")
    comments = relationship("Comment", back_populates="document")


class DocumentEmbedding(Base):
    __tablename__ = "document_embeddings"
    
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    embedding = Column(JSON, nullable=False)  # Vector embedding as JSON array
    chunk_index = Column(Integer, nullable=False)  # For chunked documents
    chunk_text = Column(Text, nullable=False)  # The text that was embedded
    
    # Relationships
    document = relationship("Document", back_populates="embeddings")


class Comment(Base):
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    user_id = Column(Integer, nullable=False)  # In a real app, this would be a foreign key
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    document = relationship("Document", back_populates="comments")


class SearchQuery(Base):
    __tablename__ = "search_queries"
    
    id = Column(Integer, primary_key=True, index=True)
    query = Column(String, nullable=False)
    user_id = Column(Integer, nullable=False)
    results_count = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
