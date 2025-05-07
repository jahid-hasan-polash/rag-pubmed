from app.services.embedding_service import EmbeddingService
from app.services.document_service import DocumentService
from app.services.llm_service import LLMService
from app.services.retrieval_service import RetrievalService
from app.utils.vector_store import VectorStore
from app.core.config import settings


# Service instances
_embedding_service = None
_document_service = None
_llm_service = None
_retrieval_service = None


def get_embedding_service():
    """Get or create the embedding service."""
    global _embedding_service
    if _embedding_service is None:
        _embedding_service = EmbeddingService(model_name=settings.EMBEDDING_MODEL)
    return _embedding_service


def get_vector_store():
    """Get or create the vector store."""
    embedding_service = get_embedding_service()
    return VectorStore(dimension=embedding_service.get_dimension())


def get_document_service():
    """Get or create the document service."""
    global _document_service
    if _document_service is None:
        embedding_service = get_embedding_service()
        vector_store = get_vector_store()
        _document_service = DocumentService(
            embedding_service=embedding_service,
            vector_store=vector_store
        )
    return _document_service


def get_llm_service():
    """Get or create the LLM service."""
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService(model_name=settings.LLM_MODEL)
    return _llm_service


def get_retrieval_service():
    """Get or create the retrieval service."""
    global _retrieval_service
    if _retrieval_service is None:
        document_service = get_document_service()
        llm_service = get_llm_service()
        _retrieval_service = RetrievalService(
            document_service=document_service,
            llm_service=llm_service
        )
    return _retrieval_service