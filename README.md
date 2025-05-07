# RAG PubMed: A Minimal Retrieval-Augmented Generation Pipeline

This project implements a minimal Retrieval-Augmented Generation (RAG) pipeline that retrieves relevant documents based on natural language queries and generates context-aware answers using a Large Language Model (LLM).

## Features

- Document embedding using SentenceTransformers
- Vector storage and similarity search with FAISS
- LLM-based answer generation using OpenAI's API
- FastAPI endpoints for document ingestion and querying
- Dockerized setup for easy deployment

## Architecture

The application follows a modular architecture with the following main components:

1. **Document Processing**: Handles document ingestion, storage, and retrieval
2. **Embedding Service**: Generates vector embeddings for documents and queries
3. **Vector Store**: Manages and indexes document embeddings for similarity search
4. **LLM Service**: Interfaces with OpenAI's API to generate answers
5. **Retrieval Service**: Orchestrates the end-to-end retrieval and answer generation
6. **API Layer**: Provides HTTP endpoints for interacting with the system

## Setup

### Prerequisites

- Docker and Docker Compose
- OpenAI API key (for LLM-based answer generation)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/jahid-hasan-polash/rag-pubmed
   cd rag-pubmed
   ```

2. Create a `.env` file with your OpenAI API key:
   ```bash
   echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
   ```

3. Build and start the Docker container:
   ```bash
   docker compose up -d --build
   ```

4. The API will be available at http://localhost:8000

## Data Sources

This project uses abstracts from the following PubMed publications:

1. ["The role of ret gene in the pathogenesis of Hirschsprung disease"](https://pubmed.ncbi.nlm.nih.gov/15858239/)
2. ["Differential contributions of rare and common, coding and noncoding Ret mutations to multifactorial Hirschsprung disease liability"](https://pubmed.ncbi.nlm.nih.gov/20598273/)
3. ["Hirschsprung disease: etiologic implications of unsuccessful prenatal diagnosis"](https://pubmed.ncbi.nlm.nih.gov/6650562/)

## Design Choices

### Embedding Model

We chose the `all-MiniLM-L6-v2` model from SentenceTransformers due to its balance of performance and efficiency. It produces 384-dimensional embeddings that capture semantic meaning well while remaining computationally lightweight.

### Vector Store Implementation

Rather than using a full-featured vector database, we implemented a lightweight vector store using FAISS. This approach provides:
- Fast similarity search with minimal overhead
- Simple persistence mechanism (pickle for metadata, FAISS for vectors)
- No external dependencies or services required

### LLM Integration

We used OpenAI's GPT models (defaulting to gpt-3.5-turbo) for answer generation because:
- They provide high-quality answers with proper context utilization
- The API is straightforward to integrate
- The system can be easily adapted to use other models (local or cloud-based)

### Modular Architecture

The system is built with clear separation of concerns:
- Service classes handle specific functionality (embeddings, documents, LLM)
- Models define data structures and validation
- API layer focuses on request/response handling
- Configuration is externalized via environment variables

This design makes the system easier to understand, test, and extend.

## API Documentation

Detailed API documentation with interactive testing capabilities is available through Swagger UI at:

```
http://localhost:8000/docs
```

All endpoints can be explored, request/response schemas, and test API calls directly from this interface.
