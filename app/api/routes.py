from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from typing import List
import time
from app.models.document import DocumentInput, IngestResponse
from app.models.request import QueryRequest, BatchIngestRequest
from app.models.response import QueryResponse
from app.services.retrieval_service import RetrievalService
from app.core.dependencies import get_retrieval_service

router = APIRouter()


@router.post("/ingest", response_model=IngestResponse)
async def ingest_documents(
    documents: List[DocumentInput],
    retrieval_service: RetrievalService = Depends(get_retrieval_service)
):
    """
    Ingest documents into the system.
    
    - Generates embeddings for each document
    - Stores documents and embeddings in the vector store
    
    Returns the IDs of the ingested documents.
    """
    if not documents:
        raise HTTPException(status_code=400, detail="No documents provided")
    
    start_time = time.time()
    document_ids = retrieval_service.document_service.ingest_documents(documents)
    processing_time = time.time() - start_time
    
    return IngestResponse(
        status="success",
        document_ids=document_ids,
        message=f"Successfully ingested {len(document_ids)} documents in {processing_time:.2f} seconds"
    )


@router.post("/batch-ingest", response_model=IngestResponse)
async def batch_ingest_documents(
    request: BatchIngestRequest,
    retrieval_service: RetrievalService = Depends(get_retrieval_service)
):
    """
    Batch ingest multiple documents at once.
    
    Documents should be provided as a list of dictionaries with 'title', 'content', and optional 'metadata'.
    """
    if not request.documents:
        raise HTTPException(status_code=400, detail="No documents provided")
    
    start_time = time.time()
    document_ids = retrieval_service.document_service.ingest_documents(request.documents)
    processing_time = time.time() - start_time
    
    return IngestResponse(
        status="success", 
        document_ids=document_ids,
        message=f"Successfully ingested {len(document_ids)} documents in {processing_time:.2f} seconds"
    )


@router.post("/query", response_model=QueryResponse)
async def query(
    request: QueryRequest,
    retrieval_service: RetrievalService = Depends(get_retrieval_service)
):
    """
    Process a query to retrieve relevant documents and generate an answer.
    
    - Embeds the query
    - Retrieves the most relevant documents
    - Generates an answer based on the documents
    
    Returns the answer and the retrieved documents.
    """
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    response = retrieval_service.process_query(
        query=request.query,
        top_k=request.top_k,
        elaborate=request.elaborate
    )
    
    return response