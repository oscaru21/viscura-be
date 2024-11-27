from typing import Dict, Any, Tuple, List
from datetime import datetime
import cv2
import numpy as np
from fastapi import UploadFile, HTTPException
from PIL import Image
from app.features.image_filtering import ImageFilter
from app.services.photos_service import PhotosService

class FilteringService:
    def __init__(self, photos_service: PhotosService, log_path: str = "filtering-log.txt"):
        self.image_filter = ImageFilter()
        self.photos_service = photos_service
        self.log_path = log_path

    def validate_image(self, image: np.ndarray, threshold: float) -> Dict[str, Any]:
        """
        Validates an image against quality criteria.
        Returns: Dictionary with validation results.
        """
        is_blurry = self.image_filter.is_image_blurry(image)
        is_sharp = not is_blurry
        return {
            "is_sharp": is_sharp,
            "issues": {"blurry": is_blurry},
        } 
    
    def log_result(self, message: str):
        """
        Logs a message to the log file.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_path, "a") as log_file:
            log_file.write(f"[{timestamp}] {message}\n")

    def convert_to_pil_image(self, image: np.ndarray) -> Image.Image:
        """
        Converts a numpy array (OpenCV image) to a PIL Image.
        :param image: OpenCV image (numpy array).
        :return: PIL Image.
        """
        return Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    def process_and_upload_images(
        self, event_id: int, files: List[UploadFile], threshold: float
    ) -> Tuple[List[int], int, int]:
        """
        Processes images by filtering and uploading only sharp images.

        :param event_id: Event ID for uploading sharp images.
        :param files: List of image files to process.
        :param threshold: Sharpness threshold for filtering.
        :return: A tuple with uploaded image IDs, count of sharp images, and count of blurry images.
        """
        uploaded_image_ids = []
        blurred_count = 0
        sharp_count = 0
        errors = []

        for file in files:
            try:
                # Read file into memory
                file_content = file.file.read()
                np_img = np.frombuffer(file_content, np.uint8)
                image = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

                if image is None:
                    error_message = f"[ERROR] Unable to read image: {file.filename}"
                    errors.append(error_message)
                    self.log_result(error_message)
                    continue

                # Validate image quality
                validation_result = self.validate_image(image, threshold)
                if not validation_result["is_sharp"]:
                    blurred_count += 1
                    self.log_result(f"[BLURRY] {file.filename} - Identified as blurry.")
                    continue

                # Convert to PIL Image
                image_pil = self.convert_to_pil_image(image)

                # Upload sharp images
                try:
                    image_id = self.photos_service.add_photo(image_pil, event_id)
                    uploaded_image_ids.append(image_id)
                    sharp_count += 1
                    self.log_result(
                        f"[UPLOADED] {file.filename} - Uploaded successfully with ID {image_id}."
                    )
                except Exception as upload_error:
                    error_message = (
                        f"[ERROR] {file.filename} - Failed to upload: {str(upload_error)}"
                    )
                    errors.append(error_message)
                    self.log_result(error_message)
            except Exception as process_error:
                error_message = f"[ERROR] {file.filename} - Processing failed: {str(process_error)}"
                errors.append(error_message)
                self.log_result(error_message)
        # If there were errors during processing raise HTTPException
        if errors:
            raise HTTPException(
                status_code=500,
                detail=f"Errors occurred during processing: {errors}"
            )

        return uploaded_image_ids, sharp_count, blurred_count