from fastapi import FastAPI, File, UploadFile, Query, HTTPException, Depends, Form
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from typing import List, Optional
import os
import json
from fastapi.responses import FileResponse, JSONResponse
from pdfminer.high_level import extract_text
from docx import Document 

import numpy as np

from app.services.image_description_service import ImageDescriptionService
from app.services.embedding_service import EmbeddingService
from app.services.search_service import SearchService
from app.services.rag_service import RAGService
from app.services.photos_service import PhotosService
from app.services.events_service import EventsService
from app.services.feedback_service import FeedbackService
# from app.services.authorization_service import AuthorizationService
from app.services.post_service import PostService, PostCreateRequest, PostUpdateRequest
from app.services.database_service import DatabaseService
from app.services.upload_service import UploadService
from app.services.context_service import ContextService

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
content_generator = ImageDescriptionService()
embedding_service = EmbeddingService()
search_service = SearchService()
rag_service = RAGService(embedding_service)
photos_service = PhotosService(embedding_service)
events_service = EventsService()
feedback_service = FeedbackService()
upload_service = UploadService(base_upload_dir="uploads", remote_server_url="http://127.0.0.1:8000/upload")
context_service = ContextService(embedding_service)

IMAGE_DIR = "uploads/images"

### DEPENDENCIES
# Dependency to provide a database connection
def get_database_service():
    with DatabaseService() as db_service:
        yield db_service

# Dependency to provide PostService with a DatabaseService instance
def get_post_service(db: DatabaseService = Depends(get_database_service)):
    return PostService(db=db)

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
        return JSONResponse(
            status_code=404,
            content={"error": f"No images found for event ID {eventId}."}
        )
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
    return FileResponse(image_path, media_type="image/jpeg", filename=photoName)

@app.post("/events/{event_id}/photos")
async def upload_and_process_photos(
    event_id: int,
    files: List[UploadFile] = File(...),  # FastAPI expects multipart data as UploadFile
    use_remote: bool = Form(False)
):
    try:
        processed_images = []
        
        for upload_file in files:
            try:
                # Save the uploaded file to a temporary path
                temp_file_path = f"temp_{upload_file.filename}"
                with open(temp_file_path, "wb") as temp_file:
                    temp_file.write(await upload_file.read())
                
                # Process the saved file
                image = Image.open(temp_file_path)
                photo_id = photos_service.add_photo(image, event_id)
                processed_images.append({"photo_id": photo_id, "file_path": temp_file_path})

                # Clean up the temporary file
                os.remove(temp_file_path)

            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error processing file {upload_file.filename}: {str(e)}")

        return {
            "event_id": event_id,
            "message": "Photos uploaded and processed successfully",
            "processed_images": processed_images,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
    
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
    files: List[UploadFile] = File(...)
    text: Optional[str] = None

@app.post("/events/{event_id}/context")
async def upload_context(
    event_id: int,
    files: Optional[List[UploadFile]] = File(None),
    text: Optional[str] = Form(None)
):
    """
    Upload documents or add textual context for an event.
    """
    if files:
        # Process uploaded documents
        context_service.process_documents(event_id, files)

    elif text:
        # Add text as main context
        context_service.add_context(event_id, text, "main_context")

    else:
        raise HTTPException(status_code=400, detail="No files or text provided.")

    return {"message": "Context added successfully", "event_id": event_id}

@app.get("/events/{event_id}/context")
async def get_event_context(event_id: int, query: str = Query(None), n: int = Query(5)):
    # Get the similar context for the event
    similar_context = rag_service.get_similar_context(event_id, query, n)
    
    return {"similar_context": similar_context}

## POSTS ENDPOINTS
@app.post("/posts", response_model=dict)
async def create_post(request: PostCreateRequest, post_service: PostService = Depends(get_post_service)):
    """
    Endpoint to create a new post.
    """
    post_id = post_service.create_post(
        event_id=request.event_id,
        caption=request.caption,
        image_ids=request.image_ids,
        user_id=request.user_id
    )
    return {"post_id": post_id}

@app.get("/posts/{post_id}", response_model=dict)
async def get_post(post_id: int, post_service: PostService = Depends(get_post_service)):
    """
    Endpoint to get a post by its ID.
    """
    post = post_service.get_post(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@app.get("/events/{event_id}/posts", response_model=List[dict])
async def get_posts_by_event(event_id: int, post_service: PostService = Depends(get_post_service)):
    """
    Endpoint to get all posts for a given event.
    """
    posts = post_service.get_posts_by_event(event_id)
    return posts

@app.put("/posts/{post_id}", response_model=dict)
async def update_post(post_id: int, request: PostUpdateRequest, post_service: PostService = Depends(get_post_service)):
    """
    Endpoint to update an existing post.
    """
    success = post_service.update_post(
        post_id=post_id,
        event_id=request.event_id,
        caption=request.caption,
        image_ids=request.image_ids
    )
    if not success:
        raise HTTPException(status_code=404, detail="Post not found or not updated")
    return {"message": "Post updated successfully"}

@app.delete("/posts/{post_id}", response_model=dict)
async def delete_post(post_id: int, post_service: PostService = Depends(get_post_service)):
    """
    Endpoint to delete a post by its ID.
    """
    success = post_service.delete_post(post_id)
    if not success:
        raise HTTPException(status_code=404, detail="Post not found or not deleted")
    return {"message": "Post deleted successfully"}

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
