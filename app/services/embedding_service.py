from app.features.clip_embedding import ClipEmbedding

class EmbeddingService:
    def __init__(self):
        self.model = ClipEmbedding()

    def embed_image(self, image):
        embedding = self.model.transform(image, input_type='image')
        return self.model.normalize(embedding)
    
    def embed_text(self, text):
        embedding = self.model.transform(text, input_type='text')
        return self.model.normalize(embedding)