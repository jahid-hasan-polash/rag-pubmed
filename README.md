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
   git clone https://github.com/yourusername/rag-pubmed.git
   cd rag-pubmed