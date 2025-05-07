import os
import pickle
import numpy as np
import faiss
from typing import List, Tuple, Dict, Optional
from app.models.document import Document
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class VectorStore:
    """
    A lightweight vector database implementation using FAISS.
    Handles storing and retrieving document embeddings.
    """
    
    def __init__(self, dimension: int, store_path: str = None):
        """
        Initialize the vector store with a specific dimension.
        
        Args:
            dimension: Dimension of the embedding vectors
            store_path: Path to store the vector index and documents
        """
        self.dimension = dimension
        self.store_path = store_path or settings.VECTOR_STORE_PATH
        self.index = None
        self.documents = {}
        self._initialize_store()
    
    def _initialize_store(self):
        """Initialize the FAISS index and load existing data if available."""
        os.makedirs(os.path.dirname(self.store_path), exist_ok=True)
        
        index_path = f"{self.store_path}.index"
        docs_path = f"{self.store_path}.pkl"
        
        # Try to load existing index and documents
        if os.path.exists(index_path) and os.path.exists(docs_path):
            try:
                self.index = faiss.read_index(index_path)
                with open(docs_path, 'rb') as f:
                    self.documents = pickle.load(f)
                logger.info(f"Loaded {len(self.documents)} documents from {docs_path}")
            except Exception as e:
                logger.error(f"Error loading vector store: {e}")
                self._create_new_index()
        else:
            self._create_new_index()
    
    def _create_new_index(self):
        """Create a new FAISS index."""
        self.index = faiss.IndexFlatL2(self.dimension)
        self.documents = {}
        logger.info("Created new FAISS index")
    
    def add_documents(self, documents: List[Document]) -> List[str]:
        """
        Add documents to the vector store.
        
        Args:
            documents: List of Document objects with embeddings
            
        Returns:
            List of document IDs that were added
        """
        if not documents:
            return []
        
        # Extract embeddings and document IDs
        embeddings = []
        doc_ids = []
        
        for doc in documents:
            if doc.embedding is None:
                logger.warning(f"Document {doc.id} has no embedding, skipping")
                continue
            
            embeddings.append(doc.embedding)
            doc_ids.append(doc.id)
            # Store the document without its embedding to save space
            doc_copy = doc.dict()
            doc_copy.pop('embedding', None)
            self.documents[doc.id] = doc_copy
        
        if not embeddings:
            return []
        
        # Convert to numpy array and add to index
        embeddings_array = np.array(embeddings).astype('float32')
        self.index.add(embeddings_array)
        
        # Save the updated index and documents
        self._save()
        
        return doc_ids
    
    def search(self, query_embedding: np.ndarray, top_k: int = 5) -> List[Tuple[str, float]]:
        """
        Search for similar documents using a query embedding.
        
        Args:
            query_embedding: The embedding vector to search with
            top_k: Number of results to return
            
        Returns:
            List of tuples (document_id, similarity_score)
        """
        if self.index.ntotal == 0:
            return []
        
        # Ensure the query is a 2D array with shape (1, dimension)
        if len(query_embedding.shape) == 1:
            query_embedding = np.expand_dims(query_embedding, axis=0)
        
        # Search the index
        distances, indices = self.index.search(query_embedding.astype('float32'), min(top_k, self.index.ntotal))
        
        # Map results to document IDs
        results = []
        for i, idx in enumerate(indices[0]):
            if idx != -1:  # FAISS returns -1 for not enough results
                # Get the document ID at this index
                doc_id = list(self.documents.keys())[idx]
                results.append((doc_id, float(distances[0][i])))
        
        return results
    
    def get_document(self, doc_id: str) -> Optional[Dict]:
        """
        Retrieve a document by its ID.
        
        Args:
            doc_id: The document ID to retrieve
            
        Returns:
            The document as a dictionary, or None if not found
        """
        return self.documents.get(doc_id)
    
    def _save(self):
        """Save the current index and documents to disk."""
        index_path = f"{self.store_path}.index"
        docs_path = f"{self.store_path}.pkl"
        
        try:
            faiss.write_index(self.index, index_path)
            with open(docs_path, 'wb') as f:
                pickle.dump(self.documents, f)
            logger.info(f"Saved vector store with {len(self.documents)} documents")
        except Exception as e:
            logger.error(f"Error saving vector store: {e}")
            
    def __len__(self):
        """Return the number of documents in the store."""
        return len(self.documents)