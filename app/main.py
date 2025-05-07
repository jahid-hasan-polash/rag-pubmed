import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time
import os
from app.api.routes import router
from app.core.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description=settings.DESCRIPTION,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api")


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware to log request timing."""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(f"Request to {request.url.path} took {process_time:.2f} seconds")
    return response


@app.get("/")
async def root():
    """Root endpoint to check if the API is running."""
    return {
        "message": "PubMed RAG API is running",
        "docs": "/docs",
        "endpoints": {
            "ingest": "/api/ingest",
            "batch_ingest": "/api/batch-ingest",
            "query": "/api/query"
        }
    }


@app.on_event("startup")
async def startup_event():
    """Startup event to perform initialization tasks."""
    logger.info("Starting up PubMed RAG API...")
    
    # Create data directories if they don't exist
    os.makedirs(settings.RAW_DOCUMENTS_PATH, exist_ok=True)
    os.makedirs(settings.PROCESSED_DOCUMENTS_PATH, exist_ok=True)
    os.makedirs(os.path.dirname(settings.VECTOR_STORE_PATH), exist_ok=True)
    
    logger.info(f"Using embedding model: {settings.EMBEDDING_MODEL}")
    logger.info(f"Vector store path: {settings.VECTOR_STORE_PATH}")
    logger.info(f"LLM model: {settings.LLM_MODEL}")
    
    # Check if OpenAI API key is set
    if not settings.OPENAI_API_KEY and not os.environ.get("OPENAI_API_KEY"):
        logger.warning("OPENAI_API_KEY not set. LLM functionality will be limited.")


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event to perform cleanup tasks."""
    logger.info("Shutting down PubMed RAG API...")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)