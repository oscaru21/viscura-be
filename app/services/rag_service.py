import json
from app.services.embedding_service import EmbeddingService
from app.services.database_service import DatabaseService
from langchain.text_splitter import RecursiveCharacterTextSplitter

class RAGService:
    def __init__(self, embedding_service: EmbeddingService, chunk_size=500, chunk_overlap=50):
        """
        Initialize RAGService.
        :param embedding_service: Instance of the EmbeddingService.
        :param chunk_size: Maximum size of each chunk (default: 500).
        :param chunk_overlap: Overlap between chunks (default: 50).
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.embedding_service = embedding_service
        self.db = DatabaseService()

    def insert_context(self, event_id: int, text: str):
        chunks = self.get_chunks(text)
        embeddings = [self.embedding_service.embed_text(chunk) for chunk in chunks]

        for chunk, embedding in zip(chunks, embeddings):
            self.db.insert_record(
                "contexts",
                {
                    "content": chunk,
                    "embedding": json.dumps(embedding.tolist()),  # Ensure this is list-serializable
                    "event_id": event_id,
                },
            )
        self.db.close()


    def get_similar_context(self, event_id: int, text: str, n=5):
        """
        Retrieves similar context from the database based on embeddings.
        :param event_id: Event identifier.
        :param text: Query text to find similar contexts.
        :param n: Number of similar records to retrieve (default: 5).
        :return: List of similar context records.
        """
        # Create embedding for the query text
        text_embedding, _ = self.embedding_service.embed_text(text)
        text_embedding = json.dumps(text_embedding.tolist()[0])
        # Retrieve similar records from the database
        similar_records = self.db.get_similar_records(
            "contexts", "embedding", event_id, text_embedding, n
        )
        self.db.close()
        return similar_records

    def get_chunks(self, text: str):
        """
        Splits text into smaller chunks using RecursiveCharacterTextSplitter.
        :param text: Input text to be chunked.
        :return: List of text chunks.
        """
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )
        chunks = text_splitter.split_text(text)
        return chunks
    