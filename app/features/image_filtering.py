import cv2
import numpy as np

class ImageFilter:
    def __init__(self, threshold=100.0):
        self.threshold = threshold

    def variance_of_laplacian(self, image):
        """
        Compute the Laplacian variance of the image
        Returns a focus measure, where higher values mean more in-focus
        """
        return cv2.Laplacian(image, cv2.CV_64F).var()

    def is_image_blurry(self, image):
        """
        Determines if an image is blurry based on the variance of laplacian
        Returns: True if image is blurry, False otherwise
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        fm = self.variance_of_laplacian(gray)
        return fm < self.threshold

    def check_brightness(self, image, min_brightness=40, max_brightness=220):
        """
        Check if image brightness is within acceptable range
        Returns: True if brightness is acceptable, False otherwise
        """
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        brightness = hsv[..., 2].mean()
        return min_brightness <= brightness <= max_brightness 