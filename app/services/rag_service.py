import json
from app.services.embedding_service import EmbeddingService
from app.services.database_service import DatabaseService

class RAGService:
    def __init__(self, embedding_service: EmbeddingService, max_length=10):
        self.max_length = max_length
        self.embedding_service = embedding_service
        
    def insert_context(self, event_id: int, text:str):
        # divide the text into chunks
        chunks = self.get_chunks(text)
        # create the embeddings
        embeddings = [self.embedding_service.embed_text(chunk) for chunk in chunks]
        # insert the dataframe into postgres db
        db = DatabaseService()
        for chunk, embedding in zip(chunks, embeddings):
            db.insert_record("embeddings", {"content": chunk, "embedding": json.dumps(embedding[0].tolist()[0]), "event_id": event_id})
        db.close()
        
    def get_similar_context(self, event_id: int, text: str, n=5):
        # get the embeddings for the text
        text_embedding, _ = self.embedding_service.embed_text(text)
        text_embedding = json.dumps(text_embedding.tolist()[0])
        # get the similar records from the database
        db = DatabaseService()
        similar_records = db.get_similar_records("embeddings", "embedding", event_id, text_embedding, n)

        db.close()
        return similar_records
        
    def get_chunks(self, text: str):
        # Split the text into chunks
        # The model has a maximum token limit, so we need to split the text
        # into smaller chunks if it exceeds the limit
        words = text.split()
        text_chunks = [' '.join(words[i:i+self.max_length]) for i in range(0, len(words), self.max_length)]
        return text_chunks
    