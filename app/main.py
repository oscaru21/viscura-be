from fastapi import FastAPI, File, UploadFile, Query, Form, HTTPException, Depends, Form, Security, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.openapi.models import APIKey
from fastapi.openapi.models import SecuritySchemeType
from fastapi.openapi.utils import get_openapi
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from PIL import Image
from typing import List, Optional, Union
import os
from jose import jwt


from pdfminer.high_level import extract_text
from docx import Document 

from app.services.image_description_service import ImageDescriptionService
from app.services.embedding_service import EmbeddingService
from app.services.search_service import SearchService
from app.services.photos_service import PhotosService
from app.services.events_service import EventsService
from app.services.feedback_service import FeedbackService
from app.services.filter_service import FilteringService
# from app.services.authorization_service import AuthorizationService
from app.services.post_service import PostService, PostCreateRequest, PostUpdateRequest
from app.services.database_service import DatabaseService
from app.services.upload_service import UploadService
from app.services.context_service import ContextService
from app.services.content_generation_service import ContentGenerationService, CaptionRequest    
from app.services.auth_service import AuthService
from app.schemas.auth import UserRegisterRequest, UserLoginRequest, TokenResponse   

from pydantic import BaseModel

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.


app = FastAPI()
security_scheme = HTTPBearer()

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


IMAGE_DIR = "uploads/images"
MODEL_NAME = 'microsoft/Phi-3.5-mini-instruct'
SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
ALGORITHM = "HS256"

# define services
image_description_service = ImageDescriptionService()
embedding_service = EmbeddingService()
search_service = SearchService()
photos_service = PhotosService()
events_service = EventsService()
feedback_service = FeedbackService()
upload_service = UploadService(base_upload_dir="uploads", remote_server_url="http://127.0.0.1:8000/upload")
context_service = ContextService()
content_generation_service = ContentGenerationService(model_name=MODEL_NAME)
filtering_service = FilteringService(photos_service=photos_service)
auth_service = AuthService()

@app.middleware("http")
async def enforce_authentication(request: Request, call_next):
    # Exempt specific paths
    exempt_paths = [
        "/auth/login", 
        "/auth/register", 
        "/auth/logout",
        "/docs",
        "/openapi.json",
        ]
    if any(request.url.path.startswith(path) for path in exempt_paths):
        return await call_next(request)
    # Check authentication for all other paths
    try:
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise HTTPException(status_code=401, detail="Authorization header missing")
        token = auth_header.split(" ")[1]
        jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except Exception as e:
        return JSONResponse(status_code=401, content={"detail": str(e)})

    return await call_next(request)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="VISCURA Backend",
        version="1.0.0",
        description="APIs for the VISCURA project",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "HTTPBearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    for path, methods in openapi_schema["paths"].items():
        for method in methods.values():
            # Add security to all endpoints except login, register, and logout
            if path not in ["/auth/login", "/auth/register", "/auth/logout"]:
                method.setdefault("security", [{"HTTPBearer": []}])

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi



### DEPENDENCIES
# Dependency to provide a database connection
def get_database_service():
    with DatabaseService() as db_service:
        yield db_service

# Dependency to provide PostService with a DatabaseService instance
def get_post_service(db: DatabaseService = Depends(get_database_service)):
    return PostService(db=db)

# Dependency to validate the token
def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security_scheme)):
    """
    Extract the current user information from the JWT token.
    """
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"Decoded token payload: {payload}")  # Debug payload
        print(f"Decoded roles: {payload.get('roles', [])}")

        if not payload:
            raise HTTPException(status_code=401, detail="Invalid token")
        if "roles" not in payload:
            raise HTTPException(status_code=401, detail="Token missing roles")
        return payload  # Return the decoded payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
    

# Dependency to require authentication    
def require_authentication(credentials: HTTPAuthorizationCredentials = Security(security_scheme)):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if not payload:
            raise HTTPException(status_code=401, detail="Invalid token")
        return payload  # Return the decoded payload for further use
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")


# Dependency to check if the current user has at least one of the allowed roles
def require_role(*allowed_roles: str):
    def dependency(credentials: dict = Depends(get_current_user)):
        user_roles = credentials.get("roles", [])
        print(f"Roles allowed: {allowed_roles}, User roles: {user_roles}") # Debugging
        if not user_roles:
            raise HTTPException(status_code=403, detail="User has no roles assigned")
        if not any(role in allowed_roles for role in user_roles):
            raise HTTPException(status_code=403, detail="Access denied: insufficient permissions")
        return credentials  # Return the full user payload if validation passes

    return dependency
  
## PHOTOS ENDPOINTS
class Photo(BaseModel):
    id: int
    name: str
    url: str
    resolution: str

@app.get(
        "/events/{eventId}/photos",
        tags=["photos"],
        summary="Get all photos for an event",
        description="Get all photos for an event by providing the event ID.",
        response_description="List of photos"
         )
async def serve_image(
    eventId: int,
    _: dict = Depends(require_authentication)
    ):
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
    images = [{"id": int(name.split('.')[0]), "name": name, "url": f"http://localhost:8000/events/{eventId}/photos/{name}", "resolution": "1920x1080"} for name in images_names]
    return images

@app.get(
        "/events/{eventId}/photos/{photoName}",
        tags=["photos"],
        summary="Get a specific photo for an event",
        description="Get a specific photo for an event by providing the event ID and photo name.",
        response_description="Photo"
         )
async def serve_image(
    eventId: int, 
    photoName: str,
    _: dict = Depends(require_authentication)
    ):
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

@app.post(
        "/events/{eventId}/photos",
        tags=["photos"],
        summary="Upload images for an event",
        description="Upload images for an event by providing the event ID and a list of image files.",
        response_description="Success message and uploaded image IDs"
         )
async def upload_images(
    eventId: int,
    files: List[UploadFile] = File(...),
    apply_filter: bool = Form(False),
    threshold: float = Form(100.0),
    _: dict = Depends(require_role("photographer"))
    ):
    """
    Endpoint to upload images for a specific event with optional filtering for quality.
    :param eventId: Event ID for the images.
    :param files: List of image files to upload.
    :param apply_filter: Flag to apply filtering for image quality.
    :param threshold: Threshold for image quality filtering.
    :return: Success message and uploaded image IDs.
    """
    try:
        if apply_filter:
            uploaded_image_ids, sharp_count, blurred_count = filtering_service.process_and_upload_images(
                event_id=eventId, files=files, threshold=threshold
            )
        else:
            # If no filtering is applied, upload all images 
            uploaded_image_ids = []
            for file in files:
                try:
                    image = Image.open(file.file)
                    image_id = photos_service.add_photo(image, eventId)
                    uploaded_image_ids.append(image_id)
                except Exception as e:
                    raise HTTPException(
                        status_code=500,
                        detail=f"Error processing file {file.filename}: {str(e)}"
                    )

            sharp_count = len(uploaded_image_ids)
            blurred_count = 0

        return {
            "message": "Images processed and uploaded successfully.",
            "total_images": len(files),
            "blurred_count": blurred_count,
            "sharp_count": sharp_count,
            "uploaded_image_ids": uploaded_image_ids,
            "event_id": eventId
        }

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error occurred: {str(e)}"
        )

@app.delete("/events/{eventId}/photos",
            tags=["photos"],
            summary="Delete selected images from an event",
            description="Delete selected images from an event by providing a list of photo IDs.",
            response_description="Success message"
            )
async def delete_images(
    eventId: int, 
    photoIds: List[int],
    _: dict = Depends(require_role("photographer", "content manager"))
):
    for photoId in photoIds:
        photos_service.delete_photo(str(eventId), photoId)
    return {"message": "Images deleted successfully"}

@app.get(
        "/events/{eventId}/photos/search/",
        tags=["photos"],
        summary="Search images by text",
        description="Search images by text using the provided query and threshold.",
        response_description="List of image IDs"
        )
async def search_images_by_text(
    eventId: int, 
    text: str, 
    threshold: float = Query(0.5),
    _: dict = Depends(require_authentication)
    ):
    text_embedding_np, _ = embedding_service.embed_text([text])
    results = search_service.search(eventId, text_embedding_np, threshold)
    results_list = [int(item) for item in results]
    return results_list

## EVENTS ENDPOINTS

class Event(BaseModel):
    title: str
    description: str
    org_id: int

@app.post(
        "/events",
        tags=["events"],
        summary="Add an event",
        description="Add an event by providing the title, description, and organization ID.",
        response_description="Success message and event ID"
        )
async def add_event(
    event: Event,
    _: dict = Depends(require_role("content manager"))
):
    event_id = events_service.add_event(event)
    return {"event_id": event_id}

@app.get(
        "/events",
        tags=["events"],
        summary="Get all events",
        description="Get all events for an organization by providing the organization ID.",
        response_description="List of events"
        )
async def get_all_events(
    org_id: int,
    _: dict = Depends(require_authentication)
    ):
    events = events_service.get_all_events(org_id)
    return events

@app.get(
        "/events/{event_id}",
        tags=["events"],
        summary="Get an event by ID",
        description="Get an event by providing the event ID and organization ID.",
        response_description="Event details"
        )
async def get_event(
    event_id: int, 
    org_id: int,
    _: dict = Depends(require_authentication)
    ):
    event = events_service.get_event(org_id, event_id)
    return event

@app.delete(
            "/events/{event_id}",
            tags=["events"],
            summary="Delete an event",
            description="Delete an event by providing the event ID and organization ID.",
            response_description="Success message"
            )
async def delete_event(
    event_id: int, 
    org_id: int,
    _: dict = Depends(require_role("content manager"))
    ):
    events_service.delete_event(org_id, event_id)
    return {"message": "Event deleted successfully"}
    

class EventContext(BaseModel):
    files: List[UploadFile] = File(...)
    text: Optional[str] = None

@app.post(
          "/events/{event_id}/context",
          tags=["context"],
          summary="Upload context for an event",
          description="Upload documents or add textual context for an event by providing the event ID and context type.",
          response_description="Success message and event ID"
          )
async def upload_context(
    event_id: int,
    context_type: str = Query(..., description="Type of context to add: 'document' or 'main context'"),
    files: Optional[Union[List[UploadFile], str]] = File(None),
    text: Optional[str] = Form(None),
    _: dict = Depends(require_role("content manager"))
    ):
    """
    Upload documents or add textual context for an event.
    :param event_id: Event ID.
    :param context_type: Type of context to add. It can be 'document' or 'main context'.
    :param files: List of files to upload.
    :param text: Textual context to add.
    :return: Success message and event ID.
    """
    try:
        if isinstance(files, str):
            files = []
        if context_type == "document":
            if not files or not isinstance(files, list):
                raise HTTPException(
                    status_code=422,
                    detail="Files are required for 'document' context type."
                )
            context_service.process_documents(event_id, files)
        elif context_type == "main context":
            if not text:
                raise HTTPException(
                    status_code=422,
                    detail="Text is required for 'main context' type."
                )
            context_service.add_context(event_id, text, "main_context")
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid context_type '{context_type}'. Expected 'document' or 'main context'."
            )

        return {"message": "Context added successfully", "event_id": event_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@app.get(
        "/events/{event_id}/context",
        tags=["context"],
        summary="Get context for an event",
        description="Get all contexts for an event by providing the event ID.",
        response_description="List of context IDs and their types"
        )
async def get_event_context_by_event_id(
    event_id: int,
    _: dict = Depends(require_authentication)
    ):
    """
    Get all contexts associated with a specific event ID.

    :param event_id: Event identifier.
    :return: A list of context IDs and their corresponding context types.
    """
    try:
        # Fetch contexts from the database using the event ID
        db = DatabaseService()
        contexts = db.read_records("contexts", {"event_id": event_id})
        db.close()

        if not contexts:
            raise HTTPException(status_code=404, detail=f"No contexts found for event ID {event_id}")
        context_list = [{"id": context["id"], "context_type": context["context_type"]} for context in contexts]
        return {"event_id": event_id, "contexts": context_list}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving contexts: {str(e)}")


## POSTS ENDPOINTS
@app.post(
        "/posts", 
        response_model=dict,
        tags=["posts"],
        summary="Create a new post",
        description="Create a new post by providing the event ID, caption, image IDs, and user ID.",
        response_description="Post ID"
        )
async def create_post(
    request: PostCreateRequest, 
    post_service: PostService = Depends(get_post_service),
    _: dict = Depends(require_role("content manager"))
    ):
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

@app.get(
        "/posts/{post_id}", 
        response_model=dict,
        tags=["posts"],
        summary="Get a post by ID",
        description="Get a post by providing the post ID.",
        response_description="Post details"
        )
async def get_post(
    post_id: int, 
    post_service: PostService = Depends(get_post_service),
    _: dict = Depends(require_role("content manager", "content reviewer"))
    ):
    """
    Endpoint to get a post by its ID.
    """
    post = post_service.get_post(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@app.get(
        "/events/{event_id}/posts", 
        response_model=List[dict],
        tags=["posts"],
        summary="Get all posts for an event",
        description="Get all posts for an event by providing the event ID.",
        response_description="List of posts"
        )
async def get_posts_by_event(
    event_id: int, 
    post_service: PostService = Depends(get_post_service),
    _: dict = Depends(require_role("content manager", "content reviewer"))
    ):
    """
    Endpoint to get all posts for a given event.
    """
    posts = post_service.get_posts_by_event(event_id)
    return posts

@app.put(
        "/posts/{post_id}", 
        response_model=dict,
        tags=["posts"],
        summary="Update an existing post",
        description="Update an existing post by providing the post ID, event ID, caption, and image IDs.",
        response_description="Success message"
        )
async def update_post(
    post_id: int, 
    request: PostUpdateRequest, 
    post_service: PostService = Depends(get_post_service),
    _: dict = Depends(require_role("content manager"))
    ):
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

@app.delete(
            "/posts/{post_id}", 
            response_model=dict,
            tags=["posts"],
            summary="Delete a post by ID",
            description="Delete a post by providing the post ID.",
            response_description="Success message"
            )
async def delete_post(
    post_id: int, 
    post_service: PostService = Depends(get_post_service),
    _: dict = Depends(require_role("content manager"))
    ):
    """
    Endpoint to delete a post by its ID.
    """
    success = post_service.delete_post(post_id)
    if not success:
        raise HTTPException(status_code=404, detail="Post not found or not deleted")
    return {"message": "Post deleted successfully"}

### CAPTION GENERATION ENDPOINT
@app.post(
          "/posts/{post_id}/generate",
          tags=["content generation"],
          summary="Generate a post caption",
          description="Generate a caption for a post using associated images and context.",
          response_description="Generated caption, relevant context, and image descriptions"
          )
async def generate_post_caption(
    post_id: int,
    request: CaptionRequest,
    post_service: PostService = Depends(get_post_service),
    _: dict = Depends(require_role("content manager"))
    ):
    """
    Generate a caption for a post using associated images and context.

    :param post_id: Post ID to fetch associated images.
    :param user_prompt: User's main prompt for the caption.
    :param tone: Tone for the caption.
    :param max_new_tokens: Maximum length of the generated caption.
    :param post_service: Dependency injection for PostService.
    :return: Generated caption, relevant context, and image descriptions.
    """
    try:
        # Fetch the post details to retrieve the associated event ID
        post = post_service.get_post(post_id)
        if not post:
            raise HTTPException(status_code=404, detail=f"Post with ID {post_id} not found.")

        event_id = post["event_id"]  # Assuming the post object has the event_id field
        image_ids = post["image_ids"]

        # Generate descriptions for all images associated with the post
        image_descriptions = content_generation_service.get_image_descriptions(event_id, image_ids)
        # Generate the post caption
        result = content_generation_service.generate_post_caption(
            image_description=image_descriptions,
            user_prompt=request.user_prompt,
            event_id=event_id,
            tone=request.tone,
            max_new_tokens=request.max_new_tokens
        )

        return result
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating caption: {str(e)}")

## FEEDBACK ENDPOINTS
class Feedback(BaseModel):
    feedback: str
    status: str

@app.post(
          "/events/{event_id}/posts/{post_id}/feedback",
          tags=["feedback"],
          summary="Add feedback for a post",
          description="Add feedback for a post by providing the event ID, post ID, and feedback details.",
          response_description="Feedback ID"
          )
async def add_feedback(
    event_id: int, 
    post_id: int, 
    feedback: Feedback,
    _: dict = Depends(require_role("content reviewer"))
    ):
    feedback_id = feedback_service.add_feedback(event_id, post_id, feedback)
    return {"feedback_id": feedback_id}

@app.get(
        "/events/{event_id}/posts/{post_id}/feedback",
        tags=["feedback"],
        summary="Get feedback for a post",
        description="Get feedback for a post by providing the event ID and post ID.",
        response_description="Feedback details"
        )
async def get_feedback(
    event_id: int, 
    post_id: int,
    _: dict = Depends(require_role("content manager", "content reviewer"))
    ):
    feedback = feedback_service.get_feedback(event_id, post_id)
    return feedback

# @app.put("/events/{event_id}/posts/{post_id}/feedback/{feedback_id}")
# async def update_feedback(event_id: int, post_id: int, feedback_id: int, feedback: Feedback):
#     feedback_service.update_feedback(event_id, post_id, feedback_id, feedback)
#     return {"message": "Feedback updated successfully"}

@app.delete(
            "/events/{event_id}/posts/{post_id}/feedback/{feedback_id}",
            tags=["feedback"],
            summary="Delete feedback for a post",
            description="Delete feedback for a post by providing the event ID, post ID, and feedback ID.",
            response_description="Success message"
            )
async def delete_feedback(
    event_id: int, 
    post_id: int, 
    feedback_id: int,
    _: dict = Depends(require_role("content reviewer"))
    ):
    feedback_service.delete_feedback(event_id, post_id, feedback_id)
    return {"message": "Feedback deleted successfully"}

### AUTH ENDPOINTS
@app.post(
          "/auth/register", 
          response_model=TokenResponse,
          tags=["auth"],
          summary="Register a new user",
          description="Register a new user by providing the user details.",
          response_description="Access token"
          )
async def register(user_data: UserRegisterRequest):
    """
    Register a new user with the given information.
    :param user_data: User registration data
    :return: Access token for the registered user
    """
    try:
        user = auth_service.register_user(user_data)
        access_token = auth_service.create_access_token(
            data={"sub": user.email},
            roles=user.roles
        )
        return TokenResponse(access_token=access_token, token_type="bearer")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post(
          "/auth/login", 
          response_model=TokenResponse,
          tags=["auth"],
          summary="Authenticate the user",
          description="Authenticate the user by email and password and return a token if successful.",
          response_description="Access token"
          )
async def login(login_data: UserLoginRequest):
    """
    Authenticate the user by email and password and return a token if successful.
    :param login_data: User login data
    :return: Access token for the authenticated
    """
    token = auth_service.authenticate_user(login_data)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return token

@app.post(
          "/auth/logout", 
          summary="Logout the user", 
          tags=["auth"],
          description="Logout the user by blacklisting their JWT token.",
          response_description="Success message"
          )
async def logout(
    authorization: HTTPAuthorizationCredentials = Depends(security_scheme),
    auth_service: AuthService = Depends(AuthService)
):
    """
    Logout the user by blacklisting their JWT token.
    :param authorization: Bearer token for the user
    :param auth_service: AuthService dependency
    :return: Success message on logout
    """
    try:
        token = authorization.credentials
        auth_service.logout_user(token)
        return {"message": "Successfully logged out"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to logout user: {str(e)}")