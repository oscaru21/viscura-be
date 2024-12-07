from langchain.prompts import PromptTemplate
from app.services.context_service import ContextService 
from app.services.image_description_service import ImageDescriptionService
from app.services.photos_service import PhotosService
from app.services.database_service import DatabaseService
from app.services.embedding_service import EmbeddingService
from app.services.upload_service import UploadService
from typing import Optional
import json
import numpy as np
from pydantic import BaseModel
import requests
import os 

class CaptionRequest(BaseModel):
    user_prompt: str
    tone: Optional[str] = "friendly"
    max_new_tokens: Optional[int] = 50

class ContentGenerationService:
    def __init__(
            self, 
            model_name: str, 
            max_length: int = 512
            ):
        """
        Initialize the ContentGenerationService.

        :param context_service: Instance of the ContextService.
        :param photos_service: Instance of the PhotosService.
        :param image_description_service: Instance of the ImageDescriptionService.
        :param model_name: HuggingFace model name for the pipeline.
        :param max_length: Maximum length of the generated text.
        """
        self.context_service = ContextService()
        self.photos_service = PhotosService()
        self.image_description_service = ImageDescriptionService()
        self.embedding_service = EmbeddingService()
        self.max_length = max_length
        self.api_token = os.environ.get('HUGGINGFACE_API_TOKEN')
        self.model_name = model_name
        self.api_url = f"https://api-inference.huggingface.co/models/{model_name}"
        self.headers = {"Authorization": f"Bearer {self.api_token}"}
        
        self.prompt_template = PromptTemplate(
            template="""
            You are a social media assistant. Based on the provided [CONTEXT], [IMAGE_CAPTIONS] and [USER_PROMPT], create an engaging social media post caption.

            Instructions:
            - Prioritize user prompt and image descriptions.
            - Write a short, engaging caption suitable for social media.
            - Use a {tone} tone and include at least one emoji.
            - Highlight key details and exciting aspects from the context.
            
            [CONTEXT]:
            {context}

            [IMAGE_CAPTIONS]: 
            {image_description}

            [USER_PROMPT]:
            {user_prompt}

            Caption:
            """,
            input_variables=["context", "image_description", "user_prompt", "tone"]
        )

    def retrieve_context(self, event_id: int, user_prompt: str, n=3) -> str:
        """
        Retrieve relevant context from the database based on the user's prompt.
        :param event_id: Event identifier.
        :param user_prompt: User's query or main prompt.
        :param n: Number of relevant documents to retrieve.
        :return: Combined relevant context as a string.
        """
        # Create embedding for the user's prompt
        embedding_result = self.embedding_service.embed_context(user_prompt)

        if isinstance(embedding_result, tuple):
            context_embedding = embedding_result[0] 
        else:
            context_embedding = embedding_result

        context_embedding = json.dumps(context_embedding.tolist())

        # Retrieve similar records from the database
        db = DatabaseService()
        similar_records = db.get_top_k_similar_records(
            table="contexts",
            vector_column="embedding",
            event_id=event_id,
            query_vector=context_embedding
        )
        db.close()

        # Combine the content of the top `n` similar contexts into a single string
        # Keep only unique contexts
        relevant_contexts = sorted(similar_records, key=lambda x: x["similarity"], reverse=True)[:n]
        unique_contexts = list({context["content"]: context for context in relevant_contexts}.values())
        combined_context = "\n\n".join([context["content"] for context in unique_contexts])

        return combined_context
    
    def get_image_descriptions(self, event_id: int, image_ids: list):
        """
        Generate descriptions for all images associated with the post.

        :param event_id: Event ID to fetch images.
        :param image_ids: List of image IDs.
        :return: List of image descriptions.
        """
        descriptions = []
        for image_id in image_ids:
            # Fetch image embedding
            photo_record = self.photos_service.get_photo(event_id, image_id)
            image_embedding = np.array(json.loads(photo_record[0]["embedding"]))
            norm_factor = photo_record[0]["norm"]
            normalized_embedding = image_embedding * norm_factor

            # Generate image description
            description = self.image_description_service.generate_caption(normalized_embedding)
            descriptions.append(description)
        return descriptions

    def generate_post_caption(self, image_description: list, user_prompt: str, event_id: int, tone="friendly", max_new_tokens=50):
        """
        Generate a social media caption using relevant context.
        :param image_description: List of image descriptions.
        :param user_prompt: User's main prompt for the caption.
        :param event_id: Event ID for retrieving relevant context.
        :param tone: Tone for the caption. Defaults to "friendly".
        :param max_new_tokens: Maximum length of the generated caption.
        :return: Generated caption, relevant context, and full prompt.
        """
        # Combine image descriptions into a single string
        image_description_text = ", ".join(image_description)

        # Retrieve relevant context
        context = self.retrieve_context(event_id, user_prompt)

        # Construct the prompt
        formatted_prompt = self.prompt_template.format(
            context=context,
            image_description=image_description_text,
            user_prompt=user_prompt,
            tone=tone
        )

        # Generate caption using the Hugging Face Inference API
        response = requests.post(
            self.api_url,
            headers=self.headers,
            json={"inputs": formatted_prompt, "parameters": {"max_new_tokens": 100}}
        )
        response.raise_for_status()
        generated_text = response.json()[0]['generated_text']

        # Extract the caption from the generated text
        caption = generated_text[len(formatted_prompt):].strip().split('\n')[0]

        return {
            "caption": caption,
            "img_description": image_description_text,
            "relevant_context": context,
            "full_prompt": formatted_prompt
        }

