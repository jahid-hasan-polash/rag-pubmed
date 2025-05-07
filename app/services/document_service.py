import os
import uuid
import json
from typing import List, Dict, Optional, Union
from app.models.document import Document, DocumentInput
from app.services.embedding_service import EmbeddingService
from app.utils.vector_store import VectorStore
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class DocumentService:
    """Service for managing documents, including ingestion and retrieval."""
    
    def __init__(self, embedding_service: EmbeddingService = None, vector_store: VectorStore = None):
        """Initialize with embedding service and vector store."""
        self.embedding_service = embedding_service or EmbeddingService()
        
        # Initialize vector store with the embedding dimension
        dimension = self.embedding_service.get_dimension()
        self.vector_store = vector_store or VectorStore(dimension=dimension)
        
        # Ensure data directories exist
        os.makedirs(settings.RAW_DOCUMENTS_PATH, exist_ok=True)
        os.makedirs(settings.PROCESSED_DOCUMENTS_PATH, exist_ok=True)
    
    def ingest_documents(self, documents: List[Union[Document, DocumentInput, Dict]]) -> List[str]:
        """
        Ingest multiple documents, generate embeddings, and store them.
        
        Args:
            documents: List of documents to ingest
            
        Returns:
            List of document IDs that were ingested
        """
        if not documents:
            return []
        
        # Convert documents to Document objects if needed
        doc_objects = []
        for doc in documents:
            if isinstance(doc, dict):
                if 'id' not in doc:
                    doc['id'] = str(uuid.uuid4())
                doc_objects.append(Document(**doc))
            elif isinstance(doc, DocumentInput):
                doc_objects.append(Document(
                    id=str(uuid.uuid4()),
                    title=doc.title,
                    content=doc.content,
                    metadata=doc.metadata
                ))
            else:  # Already a Document object
                if not doc.id:
                    doc.id = str(uuid.uuid4())
                doc_objects.append(doc)
        
        # Generate embeddings for all documents
        contents = [doc.content for doc in doc_objects]
        embeddings = self.embedding_service.get_embeddings(contents)
        
        # Assign embeddings to documents
        for i, doc in enumerate(doc_objects):
            doc.embedding = embeddings[i].tolist()
        
        # Save raw documents for reference
        for doc in doc_objects:
            self._save_raw_document(doc)
        
        # Add documents to vector store
        added_ids = self.vector_store.add_documents(doc_objects)
        logger.info(f"Ingested {len(added_ids)} documents")
        
        return added_ids
    
    def _save_raw_document(self, document: Document):
        """Save a raw document to disk for reference."""
        doc_path = os.path.join(settings.RAW_DOCUMENTS_PATH, f"{document.id}.json")
        
        # Create a copy without the embedding to save space
        doc_dict = document.dict()
        doc_dict.pop('embedding', None)
        
        with open(doc_path, 'w') as f:
            json.dump(doc_dict, f, indent=2)
    
    def retrieve_documents(self, query: str, top_k: int = None) -> List[Dict]:
        """
        Retrieve the most relevant documents for a query.
        
        Args:
            query: The search query
            top_k: Number of documents to retrieve (default from settings)
            
        Returns:
            List of retrieved documents with similarity scores
        """
        top_k = top_k or settings.TOP_K_RETRIEVAL
        
        # Generate embedding for the query
        query_embedding = self.embedding_service.get_embeddings(query)
        
        # Search for similar documents
        results = self.vector_store.search(query_embedding, top_k=top_k)
        
        # Fetch full documents and add similarity scores
        retrieved_docs = []
        for doc_id, score in results:
            doc_data = self.vector_store.get_document(doc_id)
            if doc_data:
                doc_data['similarity_score'] = score
                retrieved_docs.append(doc_data)
        
        logger.info(f"Retrieved {len(retrieved_docs)} documents for query: {query}")
        return retrieved_docs
    
    def get_document_by_id(self, doc_id: str) -> Optional[Dict]:
        """
        Get a document by its ID.
        
        Args:
            doc_id: The document ID
            
        Returns:
            The document data or None if not found
        """
        return self.vector_store.get_document(doc_id)