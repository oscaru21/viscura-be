import json
from app.services.database_service import DatabaseService

class SearchService:
    def search(self, event_id, embedding, n=1):
        db = DatabaseService()
        embedding = json.dumps(embedding.tolist()[0])
        similar_records = db.get_similar_records("images", "embedding", event_id, embedding, n)
        db.close()
        # Return the similar records ids, similar_records are RealDictRow objects
        return [record['id'] for record in similar_records]
        
        return similar_records