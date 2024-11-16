from langchain.prompts import PromptTemplate
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
from app.services.context_service import ContextService 
from app.services.image_description_service import ImageDescriptionService
from app.services.photos_service import PhotosService
from app.services.database_service import DatabaseService
from app.services.embedding_service import EmbeddingService 
from typing import Optional
import torch
import json
import numpy as np
from pydantic import BaseModel

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
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.tokenizer.pad_token_id = self.tokenizer.eos_token_id  # Set pad_token_id
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        # Set up the HuggingFace pipeline
        self.hf_pipeline = pipeline(
            'text-generation',
            model=self.model,
            tokenizer=self.tokenizer,
            max_length=self.max_length,
            temperature=0.6,
            top_p=0.9,
            repetition_penalty=1.1,
            eos_token_id=self.tokenizer.eos_token_id,
            pad_token_id=self.tokenizer.eos_token_id,
            device=0 if torch.cuda.is_available() else -1
        )
        self.prompt_template = PromptTemplate(
            template="""
            You are a social media assistant. Based on the provided context, create an engaging social media post caption.

            Context:
            {context}

            Instructions:
            - The caption should be engaging, creative, and suitable for social media.
            - Use a friendly, enthusiastic, and conversational tone.
            - Highlight key details and exciting aspects from the context.
            - Include relevant hashtags and emojis to enhance the post.
            - Always include 1-2 emojis, do not use more than 3 emojis in a caption.

            Example:
            User Prompt: "Image description: a silver Tesla. Generate a caption for a photo of the new Tesla Model Z."
            Caption: "🚀 Experience the future with the all-new Tesla Model Z! With a 500-mile range and autonomous driving, the road ahead just got electrifying! ⚡️ #Tesla #ModelZ #ElectricRevolution"

            User Prompt:
            Image descriptions: 
            {image_description}
            Create an engaging social media post caption. For
            {user_prompt}, use a {tone} tone.

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
        print(f"embed_context output: {embedding_result}")

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
        relevant_contexts = sorted(similar_records, key=lambda x: x["similarity"], reverse=True)[:n]
        combined_context = "\n\n".join([context["content"] for context in relevant_contexts])

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
        :return: Generated caption and relevant context.
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

        # Generate caption using the HuggingFace pipeline
        outputs = self.hf_pipeline(formatted_prompt, max_new_tokens=max_new_tokens, num_return_sequences=1, do_sample=True)
        generated_text = outputs[0]['generated_text']

        # Extract the caption from the generated text
        caption = generated_text[len(formatted_prompt):].strip().split('\n')[0]

        return {
            "caption": caption,
            "relevant_context": context
        }
