import os
import json
from typing import List, Optional
from fastapi import UploadFile
from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.services.database_service import DatabaseService
from app.services.embedding_service import EmbeddingService
from app.services.upload_service import UploadService

class ContextService:
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.DOCUMENT_DIR = "uploads/documents"
        self.embedding_service = EmbeddingService()
        self.upload_service = UploadService()
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def add_document(self, event_id: int, file_name: str, file_ext: str) -> int:
        """
        Add a document to the database.
        :param event_id: ID of the event.
        :param file_name: Name of the file (without extension).
        :param file_ext: File extension.
        :return: The document ID.
        """
        db = DatabaseService()
        doc_id = db.insert_record(
            "documents",
            {
                "event_id": event_id,
                "title": file_name,
                "file_ext": file_ext,
            },
        )
        db.close()
        return doc_id

    def add_context(self, event_id: int, text: str, context_type: str, doc_id: Optional[int] = None):
        """
        Add context to the database with embeddings.
        :param event_id: ID of the event.
        :param text: Text content to add as context.
        :param context_type: Type of context ('document' or 'main_context').
        :param doc_id: Document ID (if context_type is 'document').
        """
        db = DatabaseService()
        chunks = self.split_text_into_chunks(text)
        embeddings = [self.embedding_service.embed_context(chunk) for chunk in chunks]

        for chunk, embedding in zip(chunks, embeddings):
            db.insert_record(
                "contexts",
                {
                    "event_id": event_id,
                    "doc_id": doc_id,
                    "context_type": context_type,
                    "content": chunk,
                    "embedding": json.dumps(embedding.tolist()),  # Ensure serializable
                },
            )
        db.close()

    def process_documents(self, event_id: int, files: List[UploadFile]):
        """
        Process uploaded documents: save files, extract content, and add contexts.
        :param event_id: ID of the event.
        :param files: List of uploaded files.
        """
        saved_files = self.upload_service.upload_documents(files, event_id)

        for file_path in saved_files:
            file_name, file_ext = os.path.splitext(os.path.basename(file_path))
            
            # Add document metadata to the database
            doc_id = self.add_document(event_id, file_name, file_ext)

            # Read file content and add as context
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.add_context(event_id, content, "document", doc_id)

    def split_text_into_chunks(self, text: str) -> List[str]:
        """
        Split text into smaller chunks using RecursiveCharacterTextSplitter.
        :param text: Input text.
        :return: List of text chunks.
        """
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )
        return text_splitter.split_text(text)
    
    def get_context_by_event_id(self, event_id: int) -> List[dict]:
        """
        Retrieve all contexts associated with a specific event ID.
        :param event_id: ID of the event.
        """
        db = DatabaseService()
        query = "SELECT id, context_type, content FROM contexts WHERE event_id = %s"
        contexts = db.read_records("contexts", {"event_id": event_id})
        db.close()
        return contexts

    def get_context_by_context_id(self, context_id: int) -> Optional[dict]:
        """
        Retrieve a specific context by its ID.
        :param context_id: ID of the context.
        """
        db = DatabaseService()
        context = db.read_records("contexts", {"id": context_id})
        db.close()
        return context[0] if context else None

    def get_context_by_context_type(self, event_id: int, context_type: str) -> List[dict]:
        """
        Retrieve contexts by type for a specific event.
        :param event_id: ID of the event.
        :param context_type: Type of context ('document' or 'main_context').
        """
        db = DatabaseService()
        query = "SELECT id, content FROM contexts WHERE event_id = %s AND context_type = %s"
        contexts = db.read_records("contexts", {"event_id": event_id, "context_type": context_type})
        db.close()
        return contexts
