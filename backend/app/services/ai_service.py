import openai
from typing import List, Dict, Any, Optional
from ..core.config import settings
import numpy as np
from sentence_transformers import SentenceTransformer
import logging

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        self.openai_client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        # Defer loading the embedding model until first use
        self.embedding_model = None
    
    def _get_embedding_model(self):
        """Lazy load the embedding model"""
        if self.embedding_model is None:
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        return self.embedding_model
    
    async def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for text using OpenAI or local model"""
        try:
            if settings.OPENAI_API_KEY:
                response = await self.openai_client.embeddings.acreate(
                    model="text-embedding-ada-002",
                    input=text
                )
                return response.data[0].embedding
            else:
                # Use local model as fallback
                model = self._get_embedding_model()
                embedding = model.encode(text)
                return embedding.tolist()
        except Exception as e:
            logger.warning(f"OpenAI embedding failed, using local model: {e}")
            model = self._get_embedding_model()
            embedding = model.encode(text)
            return embedding.tolist()
    
    async def generate_summary(self, text: str, max_length: int = 200) -> str:
        """Generate a summary of the text using OpenAI"""
        try:
            if not settings.OPENAI_API_KEY:
                # Simple truncation fallback
                return text[:max_length] + "..." if len(text) > max_length else text
            
            response = await self.openai_client.chat.completions.acreate(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that creates concise summaries of text content."},
                    {"role": "user", "content": f"Please summarize the following text in {max_length} characters or less:\n\n{text}"}
                ],
                max_tokens=100,
                temperature=0.3
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Summary generation failed: {e}")
            return text[:max_length] + "..." if len(text) > max_length else text
    
    async def extract_tags(self, text: str) -> List[str]:
        """Extract relevant tags from text using AI"""
        try:
            if not settings.OPENAI_API_KEY:
                # Simple keyword extraction fallback
                return self._extract_keywords(text)
            
            response = await self.openai_client.chat.completions.acreate(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that extracts relevant tags from text. Return only a comma-separated list of tags, no other text."},
                    {"role": "user", "content": f"Extract 3-5 relevant tags from this text:\n\n{text}"}
                ],
                max_tokens=50,
                temperature=0.3
            )
            tags_text = response.choices[0].message.content.strip()
            return [tag.strip() for tag in tags_text.split(",") if tag.strip()]
        except Exception as e:
            logger.error(f"Tag extraction failed: {e}")
            return self._extract_keywords(text)
    
    async def extract_entities(self, text: str) -> Dict[str, Any]:
        """Extract entities like people, dates, projects from text"""
        try:
            if not settings.OPENAI_API_KEY:
                return {"people": [], "dates": [], "projects": []}
            
            response = await self.openai_client.chat.completions.acreate(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that extracts structured information from text. Return a JSON object with keys: people, dates, projects, topics."},
                    {"role": "user", "content": f"Extract entities from this text and return as JSON:\n\n{text}"}
                ],
                max_tokens=200,
                temperature=0.3
            )
            import json
            entities_text = response.choices[0].message.content.strip()
            return json.loads(entities_text)
        except Exception as e:
            logger.error(f"Entity extraction failed: {e}")
            return {"people": [], "dates": [], "projects": [], "topics": []}
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Simple keyword extraction fallback"""
        import re
        from collections import Counter
        
        # Remove common stop words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should'}
        
        # Extract words
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        words = [word for word in words if word not in stop_words]
        
        # Get most common words
        word_counts = Counter(words)
        return [word for word, count in word_counts.most_common(5)]
    
    def calculate_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """Calculate cosine similarity between two embeddings"""
        try:
            vec1 = np.array(embedding1)
            vec2 = np.array(embedding2)
            
            dot_product = np.dot(vec1, vec2)
            norm1 = np.linalg.norm(vec1)
            norm2 = np.linalg.norm(vec2)
            
            if norm1 == 0 or norm2 == 0:
                return 0.0
            
            return dot_product / (norm1 * norm2)
        except Exception as e:
            logger.error(f"Similarity calculation failed: {e}")
            return 0.0


# Global instance
ai_service = AIService()
