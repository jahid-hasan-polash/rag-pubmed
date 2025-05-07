from pydantic import BaseModel, Field
from typing import Dict, List, Optional
import datetime


class Document(BaseModel):
    """Document model for storing and processing documents."""
    id: str
    title: str
    content: str
    metadata: Optional[Dict] = Field(default_factory=dict)
    embedding: Optional[List[float]] = None
    
    class Config:
        arbitrary_types_allowed = True


class DocumentInput(BaseModel):
    """
    Model for document ingestion requests.
    Note: Document ID will be automatically generated during ingestion.
    """
    title: str
    content: str
    metadata: Optional[Dict] = Field(default_factory=dict)


class IngestResponse(BaseModel):
    """Response model for document ingestion."""
    status: str
    document_ids: List[str]
    message: str