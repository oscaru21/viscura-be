import os
import requests
import logging
from io import BytesIO
from PIL import Image

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


def upload_photos(event_id, file_paths, use_remote=False):
    url = f"{BASE_URL}/events/{event_id}/photos"
    print(f"Uploading to URL: {url}")
    print(f"Files: {file_paths}")
    print(f"use_remote: {use_remote}")

    files = [
        ('files', (os.path.basename(file_path), open(file_path, 'rb'), 'image/jpeg'))
        for file_path in file_paths
    ]
    data = {"use_remote": str(use_remote).lower()}  # Ensure use_remote is properly passed as form-data
    try:
        response = requests.post(url, files=files, data=data)
        return response.json()
    except Exception as e:
        return {"error": str(e)}
    finally:
        # Ensure file handles are closed
        for _, (_, f, _) in files:
            f.close()




def delete_photos(event_id, photo_ids):
    url = f"{BASE_URL}/events/{event_id}/photos"
    response = requests.delete(url, json={"photoIds": photo_ids})
    return response.json()


def generate_caption(event_id, photo_id):
    url = f"{BASE_URL}/events/{event_id}/photos/{photo_id}/caption"
    response = requests.get(url)
    return response.json()


def upload_context(event_id, file_paths=None, text=None):
    url = f"{BASE_URL}/events/{event_id}/context"
    data = {"text": text} if text else {}
    files = [
        ('files', (os.path.basename(file_path), open(file_path, 'rb'), 'application/octet-stream'))
        for file_path in file_paths
    ] if file_paths else None
    response = requests.post(url, data=data, files=files)
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")
    logging.debug(f"Response Status Code: {response.status_code}")
    logging.debug(f"Response Text: {response.text}")
    return response.json()


def get_context(event_id, query=None, n=5):
    url = f"{BASE_URL}/events/{event_id}/context"
    params = {"query": query, "n": n}
    response = requests.get(url, params=params)
    return response.json()


def get_file_paths(input_path):
    """
    Get a list of file paths from the input.
    If input is a file, return a single-item list.
    If input is a directory, return all files in the directory.
    """
    if os.path.isfile(input_path):
        return [input_path]
    elif os.path.isdir(input_path):
        return [
            os.path.join(input_path, f)
            for f in os.listdir(input_path)
            if os.path.isfile(os.path.join(input_path, f))
        ]
    else:
        raise ValueError(f"Invalid path: {input_path}. Must be a file or directory.")


if __name__ == "__main__":
    print("Testing upload and retrieval endpoints for documents and photos.")
    event_id = input("Enter event ID: ")
    try:
        choice = input(
            "Choose action:\n"
            "[5] Get All Photos Metadata\n"
            "[6] Get Specific Photo\n"
            "[7] Generate Caption for a Photo\n"
            "[8] Upload Context (File/Text)\n"
            "[9] Get Context with Query\n"
            "[10] Upload Photos\n"
            "[11] Delete Photos\n"
            "Enter your choice: "
        )

        if choice == "5":
            print("Fetching all photo metadata...")
            result = get_all_photos(event_id)
            print("Photo Metadata:", result)
        elif choice == "6":
            photo_name = input("Enter the name of the photo: ")
            print("Fetching photo...")
            result = get_photo(event_id, photo_name)
            print("Photo Fetch Result:", result)
        elif choice == "7":
            photo_id = input("Enter the photo ID: ")
            print("Generating caption...")
            result = generate_caption(event_id, photo_id)
            print("Caption Result:", result)
        elif choice == "8":
            context_type = input("Upload file or provide text context? [file/text]: ").lower()
            if context_type == "file":
                input_path = input("Enter the path to the document file or folder: ")
                if not os.path.exists(input_path):
                    raise ValueError("The specified path does not exist.")
                file_paths = get_file_paths(input_path)
                print("Uploading context file(s)...")
                result = upload_context(event_id, file_paths=file_paths)
            elif context_type == "text":
                text = input("Enter the text context: ")
                print("Uploading text context...")
                result = upload_context(event_id, text=text)
            else:
                raise ValueError("Invalid context type.")
            print("Context Upload Result:", result)
        elif choice == "9":
            query = input("Enter your query: ")
            n = input("Enter the number of results to return (default 5): ")
            n = int(n) if n else 5
            print("Fetching context with query...")
            result = get_context(event_id, query=query, n=n)
            print("Context Search Result:", result)
        elif choice == "10":
            input_path = input("Enter the path to the photo file or folder: ")
            if not os.path.exists(input_path):
                raise ValueError("The specified path does not exist.")
            file_paths = get_file_paths(input_path)
            print("Uploading photos...")


            result = upload_photos(event_id, file_paths)
            print("Photo Upload Result:", result)
        elif choice == "11":
            photo_ids = input("Enter the photo IDs to delete (comma-separated): ")
            photo_ids = [int(id.strip()) for id in photo_ids.split(",")]
            print("Deleting photos...")
            result = delete_photos(event_id, photo_ids)
            print("Photo Deletion Result:", result)
        else:
            print("Invalid choice.")
    except ValueError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
