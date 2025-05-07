import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert "PubMed RAG API is running" in response.json()["message"]


def test_ingest_endpoint():
    """Test the document ingest endpoint."""
    documents = [
        {
            "title": "Test Document",
            "content": "This is a test document for testing the ingest endpoint."
        }
    ]
    
    response = client.post("/api/ingest", json=documents)
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert len(response.json()["document_ids"]) > 0


def test_batch_ingest_endpoint():
    """Test the batch document ingest endpoint."""
    request = {
        "documents": [
            {
                "title": "Test Document 1",
                "content": "This is the first test document for batch ingestion."
            },
            {
                "title": "Test Document 2",
                "content": "This is the second test document for batch ingestion."
            }
        ]
    }
    
    response = client.post("/api/batch-ingest", json=request)
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert len(response.json()["document_ids"]) == 2


def test_query_endpoint():
    """Test the query endpoint."""
    # First ingest a document
    documents = [
        {
            "title": "Hirschsprung Disease",
            "content": "Hirschsprung disease is a birth defect. It affects the nerve cells in the large intestine. These cells control the muscles that normally push food and waste through the large intestine. In Hirschsprung disease, those nerve cells are missing from part or all of the large intestine. Without these nerve cells, the large intestine cannot push material through. This causes a blockage. Stool gets stuck in the large intestine, which leads to constipation, vomiting, and swelling of the belly."
        }
    ]
    
    client.post("/api/ingest", json=documents)
    
    # Then test querying
    request = {
        "query": "What is Hirschsprung disease?",
        "top_k": 1,
        "elaborate": False
    }
    
    response = client.post("/api/query", json=request)
    assert response.status_code == 200
    assert "query" in response.json()
    assert "answer" in response.json()
    assert len(response.json()["retrieved_documents"]) == 1