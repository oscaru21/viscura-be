from typing import Dict, Any
import cv2
import numpy as np
from app.features.image_filtering import ImageFilter

class FilteringService:
    def __init__(self):
        self.image_filter = ImageFilter()

    def validate_image(self, image) -> Dict[str, Any]:
        """
        Validates an image against quality criteria
        Returns: Dictionary with validation results
        """
        # Convert image to OpenCV format if needed
        if isinstance(image, bytes):
            nparr = np.frombuffer(image, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Perform checks
        is_blurry = self.image_filter.is_image_blurry(image)
        brightness_ok = self.image_filter.check_brightness(image)

        return {
            "is_valid": not is_blurry and brightness_ok,
            "issues": {
                "blurry": is_blurry,
                "brightness": not brightness_ok
            }
        } 