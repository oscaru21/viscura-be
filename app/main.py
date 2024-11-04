from fastapi import FastAPI, File, UploadFile, Query
from PIL import Image
from typing import List
import os
from fastapi.responses import FileResponse, JSONResponse

import numpy as np

from app.services.content_generation_service import ContentGenerationService
from app.services.embedding_service import EmbeddingService
from app.services.search_service import SearchService
from app.services.rag_service import RAGService
from pydantic import BaseModel

app = FastAPI()

# define services
content_generator = ContentGenerationService()
embedding_service = EmbeddingService()
search_service = SearchService()
rag_service = RAGService(embedding_service)

embeddings_store = []  # Store the embeddings and their IDs
metadata_dict = {}  # Store the metadata for each image

IMAGE_DIR = "images"

@app.post("/upload/")
async def upload_images(files: List[UploadFile] = File(...)):
    image_ids = []
    for file in files:
        image = Image.open(file.file)
        image_embedding, norm_factor = embedding_service.embed_image(image)

        # Store the embedding and ID
        image_id = len(embeddings_store)  # Simple incremental ID
        embeddings_store.append(image_embedding)
        # Store the embedding and norm factor in the index
        search_service.repository.index.add(image_embedding.astype(np.float32))
        metadata={"norm_factor": norm_factor}
        metadata_dict[image_id] = metadata
        
        image_ids.append(image_id)
        
        # Save the image with the ID as the name
        image_path = os.path.join(IMAGE_DIR, f"{image_id}.png")
        image.save(image_path)

    return {"image_ids": image_ids}

@app.get("/caption/{image_id}")
async def generate_caption(image_id: int):
    if image_id >= len(embeddings_store):
        return {"error": "Image ID not found."}
    
    image_embedding = embeddings_store[image_id]
    norm_factor = metadata_dict[image_id]["norm_factor"]
    # comment this to show trained model
    image_embedding = (image_embedding * norm_factor).numpy()
    
    caption = content_generator.generate_caption(image_embedding)
    return {"caption": caption}

@app.get("/search/")
async def search_images_by_text(text: str, num_results: int = Query(10, alias="num_results", ge=1)):
    text_embedding_np, _ = embedding_service.embed_text([text])
    results = search_service.search(text_embedding_np, num_results)
    results_list = [int(item) for item in results[0]]
    return {"similar_images": results_list}

@app.get("/image/{image_id}")
async def serve_image(image_id: int):
    image_path = os.path.join(IMAGE_DIR, f"{image_id}.png")
    if not os.path.exists(image_path):
        return JSONResponse(status_code=404, content={"error": "Image file not found."})
    return FileResponse(image_path)

class EventContext(BaseModel):
    event_context: str

@app.post("/events/{event_id}/context")
async def add_event_context(event_id: int, event_context: EventContext):
    # Add the context embedding to the vector database
    rag_service.insert_context(event_id, event_context.event_context)
    
    return {"message": "Event context added successfully", "event_id": event_id}

@app.get("/events/{event_id}/context")
async def get_event_context(event_id: int, query: str = Query(None), n: int = Query(5)):
    # Get the similar context for the event
    similar_context = rag_service.get_similar_context(event_id, query, n)
    
    return {"similar_context": similar_context}