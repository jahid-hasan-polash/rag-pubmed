import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Union
from app.core.config import settings


class EmbeddingService:
    """Service for generating embeddings from text using SentenceTransformers."""
    
    def __init__(self, model_name: str = None):
        """Initialize with a specific model or use the default from settings."""
        self.model_name = model_name or settings.EMBEDDING_MODEL
        self.model = SentenceTransformer(self.model_name)
        self.dimension = settings.EMBEDDING_DIMENSION
    
    def get_embeddings(self, texts: Union[str, List[str]]) -> np.ndarray:
        """
        Generate embeddings for one or more texts.
        
        Args:
            texts: A single text string or a list of text strings
            
        Returns:
            Numpy array of embeddings
        """
        if isinstance(texts, str):
            texts = [texts]
        
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        return embeddings
    
    def get_dimension(self) -> int:
        """
        Get the dimension of the embedding vectors.
        
        Returns:
            Dimension size as an integer
        """
        return self.dimension