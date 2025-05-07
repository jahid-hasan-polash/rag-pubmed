# app/models/response.py
from pydantic import BaseModel
from typing import List, Dict, Optional


class RetrievedDocument(BaseModel):
    """Model for retrieved documents."""
    id: str
    title: str
    content: str
    similarity_score: float
    metadata: Optional[Dict] = None


class QueryResponse(BaseModel):
    """Response model for query requests."""
    query: str
    answer: str
    retrieved_documents: List[RetrievedDocument]
    processing_time: float