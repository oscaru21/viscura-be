import unittest
from unittest.mock import patch, MagicMock
from PIL import Image
import numpy as np
from app.services.photos_service import PhotosService
import json

class TestPhotosService(unittest.TestCase):
    
    @patch('app.services.photos_service.DatabaseService')
    @patch('app.services.photos_service.EmbeddingService')
    @patch('app.services.photos_service.UploadService')
    def test_add_photo(self, MockUploadService, MockEmbeddingService, MockDatabaseService):
        # Create mock instances
        mock_db = MockDatabaseService.return_value
        mock_embedding_service = MockEmbeddingService.return_value
        mock_upload_service = MockUploadService.return_value
        
        # Set up the mock return values
        mock_embedding_service.embed_image.return_value = (np.array([0.1, 0.2, 0.3]), MagicMock())
        mock_embedding_service.embed_image.return_value[1].numpy.return_value = np.array([0.5])
        mock_db.insert_record.return_value = 1
        
        # Create a test image
        photo = Image.new('RGB', (100, 100))
        
        # Initialize the PhotosService
        service = PhotosService()
        
        # Call the add_photo method
        image_id = service.add_photo(photo, event_id=123)
        
        # Assertions
        self.assertEqual(image_id, 1)
        mock_db.insert_record.assert_called_once()
        mock_upload_service.upload_images.assert_called_once()

if __name__ == '__main__':
    unittest.main()