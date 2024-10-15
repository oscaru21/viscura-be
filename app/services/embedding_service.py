from app.features.clip_embedding import ClipEmbedding
import numpy as np

class EmbeddingService:
    def __init__(self):
        self.model = ClipEmbedding()

    def embed_image(self, image) -> np.ndarray:
        return self.model.transform(image, input_type='image')
    
    def embed_text(self, text) -> np.ndarray:
        return self.model.transform(text, input_type='text')