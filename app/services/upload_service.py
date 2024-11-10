import os
from typing import List, Optional, Union
from fastapi import UploadFile, HTTPException
from io import BytesIO
from PIL import Image
import requests

class UploadService:
    def __init__(self, base_upload_dir: str = "uploads", remote_server_url: str = None):
        """
        Initialize the upload service.
        :param base_upload_dir: Base directory for all uploads. Defaults to "uploads".
        :param remote_server_url: URL of the remote server for file uploads.
        """
        self.base_upload_dir = base_upload_dir
        self.remote_server_url = remote_server_url
        self.images_dir = os.path.join(self.base_upload_dir, "images")
        self.documents_dir = os.path.join(self.base_upload_dir, "documents")

        # Ensure the necessary directories exist
        self._create_directory(self.base_upload_dir)
        self._create_directory(self.images_dir)
        self._create_directory(self.documents_dir)

    def _create_directory(self, path: str):
        """Create a directory if it doesn't exist."""
        if not os.path.exists(path):
            os.makedirs(path)

    def upload_documents(self, files: List[UploadFile], event_id: int, use_remote: bool = False) -> List[str]:
        """
        Upload documents to the server
        :param files: List of context documents to upload
        :param event_id: Event ID
        :param use_remote: True if upload destination is remote server than the local file system

        """
        event_dir = os.path.join(self.documents_dir, str(event_id))
        self._create_directory(event_dir)
        
        saved_files = []
        for file in files:
            file_path = os.path.join(event_dir, file.filename)
            with open(file_path, "wb") as f:
                f.write(file.file.read())
            saved_files.append(file_path)

        return saved_files

    def upload_images(
        self,
        files: List[Union[UploadFile, BytesIO, Image.Image]],
        event_id: int,
        photo_names: Optional[List[str]] = None
    ) -> List[str]:
        """
        Upload images to the server, supporting PIL.Image, BytesIO, and UploadFile.
        :param files: List of image files (PIL.Image, BytesIO, or UploadFile).
        :param event_id: Event ID for directory organization.
        :param photo_names: Optional custom names for the files.
        :return: List of saved file paths.
        """
        event_dir = os.path.join(self.images_dir, str(event_id))
        self._create_directory(event_dir)
        
        saved_files = []
        for idx, file in enumerate(files):
            # Determine the file name
            photo_name = photo_names[idx] if photo_names and idx < len(photo_names) else f"image_{idx}.png"
            file_path = os.path.join(event_dir, photo_name)

            # Handle PIL.Image
            if isinstance(file, Image.Image):
                with open(file_path, "wb") as f:
                    photo_io = BytesIO()
                    file.save(photo_io, format="PNG")
                    photo_io.seek(0)
                    f.write(photo_io.read())
            elif isinstance(file, BytesIO):
                with open(file_path, "wb") as f:
                    f.write(file.read())
            elif isinstance(file, UploadFile):
                with open(file_path, "wb") as f:
                    f.write(file.file.read())
            else:
                raise HTTPException(status_code=400, detail=f"Unsupported file type: {type(file)}")
            
            saved_files.append(file_path)


    def _upload_to_remote(self, file: UploadFile):
        """
        Upload a single file to the remote server.
        :param file: File to be uploaded.
        :return: Response from the remote server.
        """
        files = {"file": (file.filename, file.file, file.content_type)}
        response = requests.post(self.remote_server_url, files=files)
        return response

    def validate_file_type(self, file: UploadFile, allowed_extensions: List[str]):
        if not any(file.filename.lower().endswith(ext) for ext in allowed_extensions):
            raise HTTPException(status_code=400, detail=f"Unsupported file type for {file.filename}")
