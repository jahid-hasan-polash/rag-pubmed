import os
import time
from typing import List, Dict, Optional
import logging
import openai
from app.core.config import settings

logger = logging.getLogger(__name__)


class LLMService:
    """Service for interacting with Language Models to generate answers."""
    
    def __init__(self, model_name: str = None, api_key: str = None):
        """
        Initialize the LLM service with a specific model and API key.
        
        Args:
            model_name: Name of the LLM model to use
            api_key: API key for the LLM service
        """
        self.model_name = model_name or settings.LLM_MODEL
        
        # Set OpenAI API key from arguments, settings, or environment
        api_key = api_key or settings.OPENAI_API_KEY or os.environ.get("OPENAI_API_KEY")
        if api_key:
            openai.api_key = api_key
        else:
            logger.warning("No OpenAI API key provided. LLM functionality may be limited.")
    
    def generate_answer(self, query: str, context_docs: List[Dict], elaborate: bool = False) -> str:
        """
        Generate an answer based on the query and retrieved documents.
        
        Args:
            query: The user's query
            context_docs: List of relevant documents to use as context
            elaborate: Whether to provide a more detailed answer
            
        Returns:
            Generated answer text
        """
        if not openai.api_key:
            return "Error: OpenAI API key not configured. Please set OPENAI_API_KEY."
        
        # Prepare context from documents
        context = self._prepare_context(context_docs)
        
        # Create system prompt with instructions
        system_prompt = self._create_system_prompt(elaborate)
        
        # Create user prompt with query and context
        user_prompt = self._create_user_prompt(query, context)
        
        try:
            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.5,
                max_tokens=1000,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
            
            answer = response.choices[0].message.content.strip()
            logger.info(f"Generated answer of length {len(answer)}")
            return answer
        
        except Exception as e:
            logger.error(f"Error generating answer: {e}")
            return f"Error generating answer: {str(e)}"
    
    def _prepare_context(self, documents: List[Dict]) -> str:
        """
        Prepare context string from retrieved documents.
        
        Args:
            documents: List of retrieved documents
            
        Returns:
            Formatted context string
        """
        context_parts = []
        
        for i, doc in enumerate(documents, 1):
            context_parts.append(f"Document {i}:")
            context_parts.append(f"Title: {doc.get('title', 'Untitled')}")
            context_parts.append(f"Content: {doc.get('content', '')}")
            context_parts.append(f"Relevance Score: {doc.get('similarity_score', 0):.4f}")
            context_parts.append("")  # Empty line between documents
        
        return "\n".join(context_parts)
    
    def _create_system_prompt(self, elaborate: bool) -> str:
        """
        Create the system prompt for the LLM.
        
        Args:
            elaborate: Whether to instruct the LLM to provide more detailed answers
            
        Returns:
            System prompt string
        """
        if elaborate:
            return """You are a medical research assistant with expertise in genetics and medicine. 
            Your task is to provide comprehensive, detailed answers based on the scientific documents provided as context.
            Include relevant medical terminology and explain concepts thoroughly.
            Always cite the specific documents you're drawing information from in your answer.
            If the context doesn't contain enough information to answer fully, clearly state this limitation."""
        else:
            return """You are a medical research assistant with expertise in genetics and medicine.
            Your task is to answer questions concisely based on the scientific documents provided as context.
            Be accurate and focus on the key information relevant to the query.
            Always cite the specific documents you're drawing information from in your answer.
            If the context doesn't contain enough information to answer the query, clearly state this limitation."""
    
    def _create_user_prompt(self, query: str, context: str) -> str:
        """
        Create the user prompt combining the query and context.
        
        Args:
            query: The user's query
            context: The context string prepared from documents
            
        Returns:
            User prompt string
        """
        return f"""Question: {query}

Context information from relevant documents:
{context}

Please answer the question based on the context information provided above."""