from pydantic import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    APP_NAME: str = "RAG PubMed API"
    DESCRIPTION: str = "Retrieval-Augmented Generation for PubMed documents"
    
    # Embedding settings
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"  # SentenceTransformers model
    EMBEDDING_DIMENSION: int = 384  # Dimension for this model
    
    # Vector store settings
    VECTOR_STORE_PATH: str = "data/processed/vector_store"
    
    # LLM settings
    LLM_MODEL: str = "gpt-3.5-turbo"  # Default LLM model
    OPENAI_API_KEY: Optional[str] = None
    
    # Document settings
    RAW_DOCUMENTS_PATH: str = "data/raw"
    PROCESSED_DOCUMENTS_PATH: str = "data/processed"
    TOP_K_RETRIEVAL: int = 2  # Number of documents to retrieve

    class Config:
        env_file = ".env"


settings = Settings()