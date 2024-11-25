import os
import requests
import logging
from io import BytesIO

logging.basicConfig(level=logging.DEBUG)

BASE_URL = "http://127.0.0.1:8000"

def get_all_photos(event_id):
    url = f"{BASE_URL}/events/{event_id}/photos"
    response = requests.get(url)
    return response.json()

def get_photo(event_id, photo_name):
    url = f"{BASE_URL}/events/{event_id}/photos/{photo_name}"
    response = requests.get(url)
    if response.status_code == 200:
        photo_path = f"downloaded_{photo_name}"
        with open(photo_path, "wb") as f:
            f.write(response.content)
        return {"message": "Photo downloaded successfully", "file_path": photo_path}
    return response.json()

def upload_photos(event_id, file_paths):
    url = f"{BASE_URL}/events/{event_id}/photos"
    files = [('files', (os.path.basename(file_path), open(file_path, 'rb'), 'image/jpeg')) for file_path in file_paths]
    try:
        response = requests.post(url, files=files)
        return response.json()
    finally:
        for _, (_, f, _) in files:
            f.close()

def delete_photos(event_id, photo_ids):
    url = f"{BASE_URL}/events/{event_id}/photos"
    response = requests.delete(url, json={"photoIds": photo_ids})
    return response.json()

def generate_caption(post_id, user_prompt, tone="friendly", max_new_tokens=50):
    url = f"{BASE_URL}/posts/{post_id}/generate"
    data = {"user_prompt": user_prompt, "tone": tone, "max_new_tokens": max_new_tokens}
    response = requests.post(url, json=data)
    return response.json()

def upload_context(event_id, file_paths=None, text=None):
    url = f"{BASE_URL}/events/{event_id}/context"
    params = {"context_type": "document" if file_paths else "main context"}
    data = {"text": text} if text else {}
    files = [('files', (os.path.basename(file_path), open(file_path, 'rb'), 'application/octet-stream')) for file_path in file_paths] if file_paths else None
    try:
        response = requests.post(url, params=params, data=data, files=files)
        return response.json()
    finally:
        if files:
            for _, (_, f, _) in files:
                f.close()

def get_context(event_id):
    url = f"{BASE_URL}/events/{event_id}/context"
    response = requests.get(url)
    return response.json()

def create_post(event_id, caption, image_ids, user_id):
    url = f"{BASE_URL}/posts"
    data = {"event_id": event_id, "caption": caption, "image_ids": image_ids, "user_id": user_id}
    response = requests.post(url, json=data)
    return response.json()

def delete_post(post_id):
    url = f"{BASE_URL}/posts/{post_id}"
    response = requests.delete(url)
    return response.json()

def test_all_endpoints():
    event_id = input("Enter Event ID: ")
    try:
        # Test upload photos
        input_path = input("Enter path to photos (file or folder): ")
        file_paths = [os.path.join(input_path, f) for f in os.listdir(input_path)] if os.path.isdir(input_path) else [input_path]
        print("Uploading photos...")
        upload_result = upload_photos(event_id, file_paths)
        print("Photo Upload Result:", upload_result)

        # Get all photos
        print("Fetching all photos...")
        photos = get_all_photos(event_id)
        print("All Photos:", photos)

        # Test fetching a single photo
        if photos:
            print("Fetching a specific photo...")
            photo_name = photos[0]["name"]
            photo_result = get_photo(event_id, photo_name)
            print("Photo Fetch Result:", photo_result)

        # Upload context (text or files)
        context_type = input("Upload context as file or text? [file/text]: ").strip().lower()
        if context_type == "file":
            input_path = input("Enter path to context files (file or folder): ")
            file_paths = [os.path.join(input_path, f) for f in os.listdir(input_path)] if os.path.isdir(input_path) else [input_path]
            print("Uploading context files...")
            context_result = upload_context(event_id, file_paths=file_paths)
        elif context_type == "text":
            text = input("Enter context text: ")
            print("Uploading text context...")
            context_result = upload_context(event_id, text=text)
        else:
            context_result = {"error": "Invalid context type."}
        print("Context Upload Result:", context_result)

        # Fetch context
        print("Fetching context...")
        context_data = get_context(event_id)
        print("Context Data:", context_data)

        # Create a post
        caption = input("Enter caption for the post: ")
        user_id = input("Enter User ID: ")
        print("Creating a post...")
        create_post_result = create_post(event_id, caption, [p["id"] for p in photos], user_id)
        print("Post Creation Result:", create_post_result)

        # Generate caption for a post
        if "post_id" in create_post_result:
            post_id = create_post_result["post_id"]
            user_prompt = input("Enter user prompt for caption generation: ")
            print("Generating caption...")
            caption_result = generate_caption(post_id, user_prompt)
            print("Generated Caption Result:", caption_result)

        # Delete photos
        if photos:
            print("Deleting photos...")
            delete_photo_result = delete_photos(event_id, [p["id"] for p in photos])
            print("Photo Deletion Result:", delete_photo_result)

    except Exception as e:
        print(f"Error during testing: {str(e)}")

if __name__ == "__main__":
    test_all_endpoints()
