"""
AI Assistant Module with RAG (Retrieval-Augmented Generation)
Uses Gemini AI and ChromaDB for document querying
"""

import os
import google.generativeai as genai
from typing import List, Dict, Optional, Union
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import numpy as np
from pathlib import Path
import json
from datetime import datetime


class DocumentVectorizer:
    """Handles document vectorization and storage"""
    
    def __init__(
        self,
        collection_name: str = "documents",
        persist_directory: str = "./chroma_db",
        embedding_model: str = "all-MiniLM-L6-v2"
    ):
        """
        Initialize Document Vectorizer
        
        Args:
            collection_name: Name of the ChromaDB collection
            persist_directory: Directory to persist vector database
            embedding_model: Sentence transformer model for embeddings
        """
        self.collection_name = collection_name
        self.persist_directory = persist_directory
        
        # Initialize ChromaDB client
        self.chroma_client = chromadb.PersistentClient(path=persist_directory)
        
        # Get or create collection
        self.collection = self.chroma_client.get_or_create_collection(
            name=collection_name,
            metadata={"description": "Document embeddings for RAG"}
        )
        
        # Initialize embedding model
        print(f"Loading embedding model: {embedding_model}...")
        self.embedding_model = SentenceTransformer(embedding_model)
        print("Embedding model loaded successfully!")
    
    def add_document(
        self,
        text: str,
        metadata: Optional[Dict] = None,
        doc_id: Optional[str] = None
    ) -> str:
        """
        Add a single document to the vector database
        
        Args:
            text: Document text content
            metadata: Optional metadata (filename, page number, etc.)
            doc_id: Optional custom document ID
            
        Returns:
            Document ID
        """
        if not text or not text.strip():
            raise ValueError("Document text cannot be empty")
        
        # Generate document ID if not provided
        if doc_id is None:
            doc_id = f"doc_{datetime.now().timestamp()}_{hash(text) % 10000}"
        
        # Generate embedding
        embedding = self.embedding_model.encode(text).tolist()
        
        # Prepare metadata
        if metadata is None:
            metadata = {}
        metadata['added_at'] = datetime.now().isoformat()
        metadata['text_length'] = len(text)
        
        # Add to collection
        self.collection.add(
            embeddings=[embedding],
            documents=[text],
            metadatas=[metadata],
            ids=[doc_id]
        )
        
        return doc_id
    
    def add_documents(
        self,
        texts: List[str],
        metadatas: Optional[List[Dict]] = None,
        doc_ids: Optional[List[str]] = None
    ) -> List[str]:
        """
        Add multiple documents to the vector database
        
        Args:
            texts: List of document texts
            metadatas: Optional list of metadata dicts
            doc_ids: Optional list of document IDs
            
        Returns:
            List of document IDs
        """
        if not texts:
            raise ValueError("Texts list cannot be empty")
        
        # Generate IDs if not provided
        if doc_ids is None:
            doc_ids = [
                f"doc_{datetime.now().timestamp()}_{i}_{hash(text) % 10000}"
                for i, text in enumerate(texts)
            ]
        
        # Generate embeddings
        print(f"Generating embeddings for {len(texts)} documents...")
        embeddings = self.embedding_model.encode(texts).tolist()
        
        # Prepare metadatas
        if metadatas is None:
            metadatas = [{} for _ in texts]
        
        for i, metadata in enumerate(metadatas):
            metadata['added_at'] = datetime.now().isoformat()
            metadata['text_length'] = len(texts[i])
        
        # Add to collection
        self.collection.add(
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas,
            ids=doc_ids
        )
        
        print(f"Added {len(texts)} documents to collection '{self.collection_name}'")
        return doc_ids
    
    def add_document_from_file(
        self,
        file_path: str,
        chunk_size: int = 1000,
        chunk_overlap: int = 200
    ) -> List[str]:
        """
        Add document from text file with chunking
        
        Args:
            file_path: Path to text file
            chunk_size: Size of each text chunk
            chunk_overlap: Overlap between chunks
            
        Returns:
            List of document IDs
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        # Split into chunks
        chunks = self._chunk_text(text, chunk_size, chunk_overlap)
        
        # Prepare metadata
        filename = Path(file_path).name
        metadatas = [
            {
                'source': filename,
                'chunk_index': i,
                'total_chunks': len(chunks)
            }
            for i in range(len(chunks))
        ]
        
        return self.add_documents(chunks, metadatas)
    
    def _chunk_text(
        self,
        text: str,
        chunk_size: int = 1000,
        chunk_overlap: int = 200
    ) -> List[str]:
        """Split text into overlapping chunks"""
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            
            if chunk.strip():
                chunks.append(chunk)
            
            start += chunk_size - chunk_overlap
        
        return chunks
    
    def search(
        self,
        query: str,
        n_results: int = 5
    ) -> Dict:
        """
        Search for relevant documents
        
        Args:
            query: Search query
            n_results: Number of results to return
            
        Returns:
            Dictionary with documents, distances, and metadatas
        """
        # Generate query embedding
        query_embedding = self.embedding_model.encode(query).tolist()
        
        # Search in collection
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        
        return {
            'documents': results['documents'][0] if results['documents'] else [],
            'distances': results['distances'][0] if results['distances'] else [],
            'metadatas': results['metadatas'][0] if results['metadatas'] else []
        }
    
    def get_collection_stats(self) -> Dict:
        """Get statistics about the collection"""
        count = self.collection.count()
        return {
            'collection_name': self.collection_name,
            'total_documents': count,
            'persist_directory': self.persist_directory
        }
    
    def delete_collection(self):
        """Delete the entire collection"""
        self.chroma_client.delete_collection(name=self.collection_name)
        print(f"Collection '{self.collection_name}' deleted")


class GeminiRAGAssistant:
    """RAG-based AI Assistant using Gemini"""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model_name: str = "gemini-2.5-flash",
        vectorizer: Optional[DocumentVectorizer] = None,
        collection_name: str = "documents"
    ):
        """
        Initialize Gemini RAG Assistant
        
        Args:
            api_key: Gemini API key (or set GEMINI_API_KEY env var)
            model_name: Gemini model name
            vectorizer: Document vectorizer instance
            collection_name: ChromaDB collection name
        """
        # Configure Gemini
        api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("Gemini API key required. Set GEMINI_API_KEY env var or pass api_key parameter")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        
        # Initialize vectorizer
        if vectorizer is None:
            self.vectorizer = DocumentVectorizer(collection_name=collection_name)
        else:
            self.vectorizer = vectorizer
        
        print(f"Gemini RAG Assistant initialized with model: {model_name}")
    
    def add_documents_to_knowledge_base(
        self,
        texts: Union[str, List[str]],
        metadatas: Optional[List[Dict]] = None
    ) -> List[str]:
        """
        Add documents to the knowledge base
        
        Args:
            texts: Single text or list of texts
            metadatas: Optional metadata for each document
            
        Returns:
            List of document IDs
        """
        if isinstance(texts, str):
            texts = [texts]
        
        return self.vectorizer.add_documents(texts, metadatas)
    
    def add_documents_from_directory(
        self,
        directory: str,
        pattern: str = "*.txt",
        chunk_size: int = 1000
    ) -> int:
        """
        Add all text files from a directory
        
        Args:
            directory: Directory path
            pattern: File pattern to match
            chunk_size: Size of text chunks
            
        Returns:
            Number of documents added
        """
        dir_path = Path(directory)
        files = list(dir_path.glob(pattern))
        
        total_docs = 0
        for file_path in files:
            print(f"Processing: {file_path.name}")
            doc_ids = self.vectorizer.add_document_from_file(
                str(file_path),
                chunk_size=chunk_size
            )
            total_docs += len(doc_ids)
        
        print(f"Total documents added: {total_docs}")
        return total_docs
    
    def query(
        self,
        question: str,
        n_context_docs: int = 3,
        temperature: float = 0.7,
        max_tokens: int = 2048
    ) -> Dict:
        """
        Query the assistant with RAG
        
        Args:
            question: User question
            n_context_docs: Number of context documents to retrieve
            temperature: Response creativity (0-1)
            max_tokens: Maximum response length
            
        Returns:
            Dictionary with answer, sources, and metadata
        """
        # Retrieve relevant documents
        search_results = self.vectorizer.search(question, n_results=n_context_docs)
        
        # Prepare context from retrieved documents
        context_docs = search_results['documents']
        context = "\n\n".join([
            f"Document {i+1}:\n{doc}"
            for i, doc in enumerate(context_docs)
        ])
        
        # Create prompt with context
        prompt = f"""Based on the following context documents, please answer the question.
If the answer cannot be found in the context, say "I don't have enough information to answer that question."

Context:
{context}

Question: {question}

Answer:"""
        
        # Generate response using Gemini
        generation_config = genai.types.GenerationConfig(
            temperature=temperature,
            max_output_tokens=max_tokens
        )
        
        response = self.model.generate_content(
            prompt,
            generation_config=generation_config
        )
        
        return {
            'question': question,
            'answer': response.text,
            'sources': search_results['metadatas'],
            'context_documents': context_docs,
            'distances': search_results['distances']
        }
    
    def chat(
        self,
        message: str,
        use_rag: bool = True,
        n_context_docs: int = 3
    ) -> str:
        """
        Simple chat interface
        
        Args:
            message: User message
            use_rag: Whether to use RAG
            n_context_docs: Number of context documents
            
        Returns:
            Assistant response
        """
        if use_rag:
            result = self.query(message, n_context_docs=n_context_docs)
            return result['answer']
        else:
            response = self.model.generate_content(message)
            return response.text
    
    def get_knowledge_base_stats(self) -> Dict:
        """Get statistics about the knowledge base"""
        return self.vectorizer.get_collection_stats()


# Convenience functions
def create_assistant(
    api_key: Optional[str] = None,
    collection_name: str = "documents"
) -> GeminiRAGAssistant:
    """
    Create a new RAG assistant
    
    Args:
        api_key: Gemini API key
        collection_name: Collection name for documents
        
    Returns:
        GeminiRAGAssistant instance
    """
    return GeminiRAGAssistant(api_key=api_key, collection_name=collection_name)


if __name__ == "__main__":
    # Example usage
    print("=== Gemini RAG Assistant Example ===\n")
    
    # Note: Set GEMINI_API_KEY environment variable first
    # export GEMINI_API_KEY="your-api-key-here"
    
    try:
        # Create assistant
        assistant = create_assistant()
        
        # Add sample documents
        print("Adding sample documents...")
        documents = [
            "Python is a high-level programming language known for its simplicity and readability.",
            "Machine learning is a subset of artificial intelligence that enables systems to learn from data.",
            "FastAPI is a modern web framework for building APIs with Python."
        ]
        assistant.add_documents_to_knowledge_base(documents)
        
        # Get stats
        stats = assistant.get_knowledge_base_stats()
        print(f"\nKnowledge base stats: {stats}\n")
        
        # Query example
        question = "What is Python?"
        print(f"Question: {question}")
        result = assistant.query(question)
        print(f"Answer: {result['answer']}\n")
        
    except ValueError as e:
        print(f"Error: {e}")
        print("\nTo use this module, set your Gemini API key:")
        print('export GEMINI_API_KEY="your-api-key-here"')
