import os
import requests

image_path = "../COMP385-CapstoneProject/Data_AutoShow2024_resized/"

def upload_files_in_directory(directory_path):
    url = "http://127.0.0.1:8000/upload/"
    files = []
    
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path):
            files.append(('files', open(file_path, 'rb')))
    
    response = requests.post(url, files=files)
    return response.json()

if __name__ == "__main__":
    result = upload_files_in_directory(image_path)
    print(result)