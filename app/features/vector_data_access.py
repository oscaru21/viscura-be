from app.models.repository import Repository
import faiss

class VectorDataRepository(Repository):
    def __init__(self, dimensions):
        self.index = faiss.IndexFlatL2(dimensions)

    def search(self, embedding, top_k=1):
        distances, indices = self.index.search(embedding, top_k)
        return indices
    
    def add(self, embedding):
        self.index.add(embedding)