# app/models/request.py
from pydantic import BaseModel, Field
from typing import Optional, List


class QueryRequest(BaseModel):
    """Model for query requests."""
    query: str
    top_k: Optional[int] = 2
    elaborate: Optional[bool] = False  # Whether to provide more detailed answers


class BatchIngestRequest(BaseModel):
    """Model for batch document ingestion."""
    documents: List[dict]