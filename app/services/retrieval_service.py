import time
from typing import Dict, List
from app.services.document_service import DocumentService
from app.services.llm_service import LLMService
from app.models.response import QueryResponse, RetrievedDocument
import logging

logger = logging.getLogger(__name__)


class RetrievalService:
    """Service for end-to-end retrieval and answer generation."""
    
    def __init__(self, document_service: DocumentService = None, llm_service: LLMService = None):
        """Initialize with document and LLM services."""
        self.document_service = document_service or DocumentService()
        self.llm_service = llm_service or LLMService()
    
    def process_query(self, query: str, top_k: int = None, elaborate: bool = False) -> QueryResponse:
        """
        Process a query: retrieve relevant documents and generate an answer.
        
        Args:
            query: The user's query string
            top_k: Number of documents to retrieve
            elaborate: Whether to generate a more detailed answer
            
        Returns:
            QueryResponse object with the answer and retrieved documents
        """
        start_time = time.time()
        
        # Retrieve relevant documents
        retrieved_docs = self.document_service.retrieve_documents(query, top_k=top_k)
        
        # Convert to RetrievedDocument model objects
        doc_models = []
        for doc in retrieved_docs:
            doc_models.append(RetrievedDocument(
                id=doc.get('id', ''),
                title=doc.get('title', ''),
                content=doc.get('content', ''),
                similarity_score=doc.get('similarity_score', 0.0),
                metadata=doc.get('metadata')
            ))
        
        # Generate answer using LLM
        answer = self.llm_service.generate_answer(query, retrieved_docs, elaborate=elaborate)
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Create response
        response = QueryResponse(
            query=query,
            answer=answer,
            retrieved_documents=doc_models,
            processing_time=processing_time
        )
        
        logger.info(f"Processed query in {processing_time:.2f} seconds")
        return response