import requests
import json
from pprint import pprint

BASE_URL = "http://127.0.0.1:8000" 


def test_upload_photos(event_id, file_paths):
    url = f"{BASE_URL}/events/{event_id}/photos"
    files = [("files", (open(file_path, "rb"))) for file_path in file_paths]
    response = requests.post(url, files=files, data={"use_remote": False})
    print("Upload Photos Response:")
    pprint(response.json())


def test_search_photos(event_id, text, threshold=0.5):
    url = f"{BASE_URL}/events/{event_id}/photos/search/"
    params = {"text": text, "threshold": threshold}
    response = requests.get(url, params=params)
    print("Search Photos Response:")
    pprint(response.json())


def test_create_post(event_id, caption, image_ids, user_id):
    url = f"{BASE_URL}/posts"
    payload = {
        "event_id": event_id,
        "caption": caption,
        "image_ids": image_ids,
        "user_id": user_id,
    }
    response = requests.post(url, json=payload)
    print("Create Post Response:")
    pprint(response.json())


def test_get_post(post_id):
    url = f"{BASE_URL}/posts/{post_id}"
    response = requests.get(url)
    print("Get Post Response:")
    pprint(response.json())


def test_generate_post_caption(post_id, user_prompt, tone="friendly", max_new_tokens=50):
    url = f"{BASE_URL}/posts/{post_id}/generate"
    payload = {
        "user_prompt": user_prompt,
        "tone": tone,
        "max_new_tokens": max_new_tokens,
    }
    response = requests.post(url, json=payload)
    try:
        pprint(response.json())
    except json.JSONDecodeError:
        print(f"Failed to decode JSON. Status code: {response.status_code}, Response text: {response.text}")



def test_upload_context(event_id, file_paths=None, text=None):
    url = f"{BASE_URL}/events/{event_id}/context"
    files = (
        [("files", open(file_path, "rb")) for file_path in file_paths] if file_paths else None
    )
    data = {"text": text} if text else {}
    response = requests.post(url, files=files, data=data)
    print("Upload Context Response:")
    pprint(response.json())


def test_get_context(event_id, query=None, n=5):
    url = f"{BASE_URL}/events/{event_id}/context"
    params = {"query": query, "n": n}
    response = requests.get(url, params=params)
    print("Get Context Response:")
    pprint(response.json())




if __name__ == "__main__":
    # Test variables
    event_id = 1
    post_id = 1
    photo_id = 1
    user_id = 1
    caption = "Sample post caption"
    image_ids = [1,2]
    file_paths = [
        r"C:\Users\lou22\Documents\SoftwareEngineeringEducation\ClassesFall2024 (6th)\Comp385 AI Capstone\rag-test\photo\IMG_5549.jpeg",
        r"C:\Users\lou22\Documents\SoftwareEngineeringEducation\ClassesFall2024 (6th)\Comp385 AI Capstone\Data_AutoShow2024_resized\IMG_4051-noise.jpeg"
        ]
    text_context = """
    The 2024 Toronto Auto Show was a great event. 
    There were many new cars and concepts on display.
    The event was held at the Metro Toronto Convention Centre.
    This year, the show is pet-friendly and great for families.
    """
    query = "dog"

    print("\n--- Upload Photos ---")
    test_upload_photos(event_id, file_paths)

    # print("\n--- Search Photos ---")
    # test_search_photos(event_id, text="car")

    print("\n--- Create Post ---")
    test_create_post(event_id, caption, image_ids, user_id)

    print("\n--- Get Post ---")
    test_get_post(post_id)

    print("\n--- Upload Context ---")
    test_upload_context(event_id, text=text_context)

    print("\n--- Generate Post Caption ---")
    test_generate_post_caption(post_id, user_prompt="tell everyone that the event is dog friendly")

    

    

