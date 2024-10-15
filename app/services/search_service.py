from app.features.vector_data_access import VectorDataRepository

class SearchService:
    def __init__(self):
        self.repository = VectorDataRepository(512)

    def search(self, embedding, top_k=1):
        return self.repository.search(embedding, top_k)