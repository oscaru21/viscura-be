from fastapi import FastAPI, File, UploadFile, Query
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from typing import List
import os
import json
from fastapi.responses import FileResponse, JSONResponse

import numpy as np

from app.services.content_generation_service import ContentGenerationService
from app.services.embedding_service import EmbeddingService
from app.services.search_service import SearchService
from app.services.rag_service import RAGService
from app.services.photos_service import PhotosService
from app.services.events_service import EventsService
from app.services.feedback_service import FeedbackService
# from app.services.authorization_service import AuthorizationService

from pydantic import BaseModel

app = FastAPI()

origins = [
    "http://localhost:4200"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# define services
content_generator = ContentGenerationService()
embedding_service = EmbeddingService()
search_service = SearchService()
rag_service = RAGService(embedding_service)
photos_service = PhotosService(embedding_service)
events_service = EventsService()
feedback_service = FeedbackService()

IMAGE_DIR = "images"

## PHOTOS ENDPOINTS
class Photo(BaseModel):
    id: int
    name: str
    url: str
    resolution: str

@app.get("/events/{eventId}/photos")
async def serve_image(eventId: int):
    """
    Get all the photos for a given event
    """
    dir = os.path.join(IMAGE_DIR, str(eventId))
    if not os.path.exists(dir):
        return []
    images_names = os.listdir(dir)
    #map the image names to Photo objects
    print(images_names)
    images = [{"id": int(name.split('.')[0]), "name": name, "url": f"http://localhost:8000/events/{eventId}/photos/{name}", "resolution": "1920x1080"} for name in images_names]
    return images

@app.get("/events/{eventId}/photos/{photoName}")
async def serve_image(eventId: int, photoName: str):
    """
    Get a specific photo for a given event
    """
    dir = os.path.join(IMAGE_DIR, str(eventId))
    if not os.path.exists(dir):
        return JSONResponse(status_code=404, content={"error": "No images found for the event."})
    image_path = os.path.join(dir, photoName)
    if not os.path.exists(image_path):
        return JSONResponse(status_code=404, content={"error": "Image not found."})
    return FileResponse(image_path)

@app.post("/events/{eventId}/photos")
async def upload_images(eventId, files: List[UploadFile] = File(...)):
    image_ids = []
    for file in files:
        image = Image.open(file.file)
        image_id = photos_service.add_photo(image, eventId)
        image_ids.append(image_id)

    return {"image_ids": image_ids}

@app.delete("/events/{eventId}/photos")
async def delete_images(eventId: int, photoIds: List[int]):
    for photoId in photoIds:
        photos_service.delete_photo(str(eventId), photoId)
    return {"message": "Images deleted successfully"}

@app.get("/events/{eventId}/photos/{photoId}/caption")
async def generate_caption(eventId: int, photoId: int):
    photo_record = photos_service.get_photo(eventId, photoId)
    # get the image embedding
    image_embedding = json.loads(photo_record[0]["embedding"])
    image_embedding = np.array(image_embedding)
    # get the norm factor
    norm_factor = photo_record[0]["norm"]
    # comment this to show trained model
    image_embedding = (image_embedding * norm_factor)
    
    caption = content_generator.generate_caption(image_embedding)
    return {"caption": caption}

@app.get("/events/{eventId}/photos/search/")
async def search_images_by_text(eventId: int, text: str, threshold: float = Query(0.5)):
    text_embedding_np, _ = embedding_service.embed_text([text])
    results = search_service.search(eventId, text_embedding_np, threshold)
    results_list = [int(item) for item in results]
    return results_list

## EVENTS ENDPOINTS

class Event(BaseModel):
    title: str
    description: str
    org_id: int

@app.post("/events")
async def add_event(event: Event):
    event_id = events_service.add_event(event)
    return {"event_id": event_id}

@app.get("/events")
async def get_all_events(org_id: int):
    events = events_service.get_all_events(org_id)
    return events

@app.get("/events/{event_id}")
async def get_event(event_id: int, org_id: int):
    event = events_service.get_event(org_id, event_id)
    return event

@app.delete("/events/{event_id}")
async def delete_event(event_id: int, org_id: int):
    events_service.delete_event(org_id, event_id)
    return {"message": "Event deleted successfully"}
    

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

## FEEDBACK ENDPOINTS
class Feedback(BaseModel):
    feedback: str
    status: str

@app.post("/events/{event_id}/posts/{post_id}/feedback")
async def add_feedback(event_id: int, post_id: int, feedback: Feedback):
    feedback_id = feedback_service.add_feedback(event_id, post_id, feedback)
    return {"feedback_id": feedback_id}

@app.get("/events/{event_id}/posts/{post_id}/feedback")
async def get_feedback(event_id: int, post_id: int):
    feedback = feedback_service.get_feedback(event_id, post_id)
    return feedback

# @app.put("/events/{event_id}/posts/{post_id}/feedback/{feedback_id}")
# async def update_feedback(event_id: int, post_id: int, feedback_id: int, feedback: Feedback):
#     feedback_service.update_feedback(event_id, post_id, feedback_id, feedback)
#     return {"message": "Feedback updated successfully"}

@app.delete("/events/{event_id}/posts/{post_id}/feedback/{feedback_id}")
async def delete_feedback(event_id: int, post_id: int, feedback_id: int):
    feedback_service.delete_feedback(event_id, post_id, feedback_id)
    return {"message": "Feedback deleted successfully"}
