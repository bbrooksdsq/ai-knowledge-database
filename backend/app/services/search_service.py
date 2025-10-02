from typing import List, Dict, Any, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from ..models.document import Document, DocumentEmbedding, SearchQuery
from ..schemas.document import SearchResult, SearchResponse
from .ai_service import ai_service
import time
import logging

logger = logging.getLogger(__name__)

class SearchService:
    def __init__(self):
        self.ai_service = ai_service
    
    async def semantic_search(
        self, 
        db: Session, 
        query: str, 
        user_id: int,
        limit: int = 10,
        filters: Optional[Dict[str, Any]] = None
    ) -> SearchResponse:
        """Perform semantic search using vector embeddings"""
        start_time = time.time()
        
        try:
            # Generate embedding for the query
            query_embedding = await self.ai_service.generate_embedding(query)
            
            # Get all document embeddings
            embeddings_query = db.query(DocumentEmbedding).join(Document)
            
            # Apply filters if provided
            if filters:
                if "file_type" in filters:
                    embeddings_query = embeddings_query.filter(Document.file_type.in_(filters["file_type"]))
                if "date_from" in filters:
                    embeddings_query = embeddings_query.filter(Document.created_at >= filters["date_from"])
                if "date_to" in filters:
                    embeddings_query = embeddings_query.filter(Document.created_at <= filters["date_to"])
                if "tags" in filters:
                    # PostgreSQL JSON query for tags
                    for tag in filters["tags"]:
                        embeddings_query = embeddings_query.filter(Document.tags.contains([tag]))
            
            embeddings = embeddings_query.all()
            
            # Calculate similarities
            similarities = []
            for embedding in embeddings:
                similarity = self.ai_service.calculate_similarity(
                    query_embedding, 
                    embedding.embedding
                )
                similarities.append((embedding, similarity))
            
            # Sort by similarity score
            similarities.sort(key=lambda x: x[1], reverse=True)
            
            # Get top results
            top_results = similarities[:limit]
            
            # Create search results
            results = []
            for embedding, score in top_results:
                # Create snippet from chunk text
                snippet = self._create_snippet(query, embedding.chunk_text)
                
                result = SearchResult(
                    document=embedding.document,
                    score=score,
                    snippet=snippet
                )
                results.append(result)
            
            # Log the search query
            search_query = SearchQuery(
                query=query,
                user_id=user_id,
                results_count=len(results)
            )
            db.add(search_query)
            db.commit()
            
            execution_time = time.time() - start_time
            
            return SearchResponse(
                query=query,
                results=results,
                total_results=len(results),
                execution_time=execution_time
            )
            
        except Exception as e:
            logger.error(f"Semantic search failed: {e}")
            return SearchResponse(
                query=query,
                results=[],
                total_results=0,
                execution_time=time.time() - start_time
            )
    
    async def keyword_search(
        self,
        db: Session,
        query: str,
        user_id: int,
        limit: int = 10,
        filters: Optional[Dict[str, Any]] = None
    ) -> SearchResponse:
        """Perform traditional keyword search"""
        start_time = time.time()
        
        try:
            # Build search query
            search_query = db.query(Document)
            
            # Add text search conditions
            search_terms = query.lower().split()
            conditions = []
            for term in search_terms:
                conditions.append(
                    or_(
                        func.lower(Document.title).contains(term),
                        func.lower(Document.content).contains(term)
                    )
                )
            
            if conditions:
                search_query = search_query.filter(or_(*conditions))
            
            # Apply filters
            if filters:
                if "file_type" in filters:
                    search_query = search_query.filter(Document.file_type.in_(filters["file_type"]))
                if "date_from" in filters:
                    search_query = search_query.filter(Document.created_at >= filters["date_from"])
                if "date_to" in filters:
                    search_query = search_query.filter(Document.created_at <= filters["date_to"])
                if "tags" in filters:
                    for tag in filters["tags"]:
                        search_query = search_query.filter(Document.tags.contains([tag]))
            
            # Execute query
            documents = search_query.limit(limit).all()
            
            # Create search results
            results = []
            for doc in documents:
                snippet = self._create_snippet(query, doc.content)
                result = SearchResult(
                    document=doc,
                    score=1.0,  # No scoring for keyword search
                    snippet=snippet
                )
                results.append(result)
            
            # Log the search query
            search_query_log = SearchQuery(
                query=query,
                user_id=user_id,
                results_count=len(results)
            )
            db.add(search_query_log)
            db.commit()
            
            execution_time = time.time() - start_time
            
            return SearchResponse(
                query=query,
                results=results,
                total_results=len(results),
                execution_time=execution_time
            )
            
        except Exception as e:
            logger.error(f"Keyword search failed: {e}")
            return SearchResponse(
                query=query,
                results=[],
                total_results=0,
                execution_time=time.time() - start_time
            )
    
    def _create_snippet(self, query: str, text: str, max_length: int = 200) -> str:
        """Create a snippet highlighting the query terms"""
        query_lower = query.lower()
        text_lower = text.lower()
        
        # Find the first occurrence of any query term
        for term in query_lower.split():
            if term in text_lower:
                start = text_lower.find(term)
                # Get context around the match
                context_start = max(0, start - 50)
                context_end = min(len(text), start + len(term) + 50)
                snippet = text[context_start:context_end]
                
                # Truncate if too long
                if len(snippet) > max_length:
                    snippet = snippet[:max_length] + "..."
                
                return snippet
        
        # Fallback: return beginning of text
        return text[:max_length] + "..." if len(text) > max_length else text
    
    async def get_related_documents(
        self,
        db: Session,
        document_id: int,
        limit: int = 5
    ) -> List[Document]:
        """Get documents related to a given document"""
        try:
            # Get the document's embeddings
            doc_embeddings = db.query(DocumentEmbedding).filter(
                DocumentEmbedding.document_id == document_id
            ).all()
            
            if not doc_embeddings:
                return []
            
            # Use the first embedding as reference
            reference_embedding = doc_embeddings[0].embedding
            
            # Find similar documents
            all_embeddings = db.query(DocumentEmbedding).filter(
                DocumentEmbedding.document_id != document_id
            ).all()
            
            similarities = []
            for embedding in all_embeddings:
                similarity = self.ai_service.calculate_similarity(
                    reference_embedding,
                    embedding.embedding
                )
                similarities.append((embedding.document, similarity))
            
            # Sort by similarity and return top results
            similarities.sort(key=lambda x: x[1], reverse=True)
            return [doc for doc, _ in similarities[:limit]]
            
        except Exception as e:
            logger.error(f"Related documents search failed: {e}")
            return []


# Global instance
search_service = SearchService()
