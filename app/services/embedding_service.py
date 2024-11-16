from app.features.clip_embedding import ClipEmbedding
from langchain_community.embeddings import HuggingFaceEmbeddings
import numpy as np

class EmbeddingService:
    def __init__(self):
        self.img_model = ClipEmbedding() # Initialize CLIP model for image embeddings
        self.txt_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


    def embed_image(self, image):
        """
        Generate an embedding for an image and normalize it.
        :param image: Input image.
        :return: Normalized image embedding.
        """
        embedding = self.img_model.transform(image, input_type='image')
        return self.img_model.normalize(embedding)
    
    def embed_text(self, text):
        """
        Generate an embedding for text queries and normalize it.
        :param text: Input text string.
        :return: Normalized text embedding.
        """
        embedding = self.img_model.transform(text, input_type='text')
        return self.model.normalize(embedding)
    
    def embed_context(self, text):
        """
        Generate an embedding for context and normalize it.
        :param text: Input text string.
        :return: Normalized text embedding as a NumPy array.
        """
        embedding = self.txt_model.embed_query(text)
        if isinstance(embedding, list):  # Convert list to NumPy array
            embedding = np.array(embedding)
        elif isinstance(embedding, float):  # Handle scalar case
            embedding = np.array([embedding])
        elif not isinstance(embedding, np.ndarray):  # Handle unexpected cases
            raise TypeError(f"Unexpected embedding type: {type(embedding)}")

        # Perform L2 normalization
        norm = np.linalg.norm(embedding)
        if norm == 0:
            raise ValueError("Cannot normalize embedding with zero norm.")
        normalized_embedding = embedding / norm

        return normalized_embedding

