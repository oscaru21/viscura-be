from app.models.embedding import Embedding
import numpy as np
from transformers import CLIPProcessor, TFAutoModel
import tensorflow as tf

class ClipEmbedding(Embedding):
    def __init__(self, model_name: str = "openai/clip-vit-base-patch32"):
        # Load CLIP model and processor
        self.clip_model = TFAutoModel.from_pretrained(model_name, from_pt=True)
        self.clip_processor = CLIPProcessor.from_pretrained(model_name)
        
        self.embedding_dimension = 512

    def transform(self, X, input_type: str = 'image'):
        if input_type == "image":
            inputs = self.clip_processor(images=X, return_tensors="tf", padding=True)
            outputs = self.clip_model.get_image_features(**inputs)
        elif input_type == "text":
            inputs = self.clip_processor(text=X, return_tensors="tf", padding=True)
            outputs = self.clip_model.get_text_features(**inputs)
        else:
            raise ValueError("Invalid input_type. Expected 'image' or 'text'.")

        # outputs = outputs / tf.norm(outputs, ord='euclidean', axis=-1, keepdims=True) #L2 normalization
        return outputs
    
    def normalize(self, embedding: np.ndarray) -> np.ndarray:
        norm_factor = tf.norm(embedding, ord='euclidean', axis=-1, keepdims=True)
        embedding = embedding / norm_factor
        return embedding.numpy(), norm_factor
    