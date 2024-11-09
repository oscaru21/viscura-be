# from app.features.caption_generation_model import CaptionGenerationModel
from app.features.caption_generation_model_v2 import CaptionGenerationModel

class  ImageDescriptionService:
    def __init__(self):
        self.caption_generation_model = CaptionGenerationModel()

    def generate_caption(self, embedding, max_length=10):
        return self.caption_generation_model.evaluate(embedding, max_length)