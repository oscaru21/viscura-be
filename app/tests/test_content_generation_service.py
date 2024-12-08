import json
from unittest.mock import patch, MagicMock
import unittest
import numpy as np
from app.services.content_generation_service import ContentGenerationService, CaptionRequest

class TestContentGenerationService(unittest.TestCase):

    @patch('psycopg2.connect')  # Mock psycopg2.connect to prevent real database connection
    @patch('app.services.content_generation_service.ContextService')
    @patch('app.services.content_generation_service.PhotosService')
    @patch('app.services.content_generation_service.ImageDescriptionService')
    @patch('app.services.content_generation_service.DatabaseService')
    @patch('app.services.content_generation_service.EmbeddingService')
    @patch('app.services.content_generation_service.requests.post')
    def setUp(self, mock_post, MockEmbeddingService, MockDatabaseService, MockImageDescriptionService, MockPhotosService, MockContextService, mock_connect):
        # Mock psycopg2 connection to return a mock connection object
        mock_db_connection = MagicMock()
        mock_connect.return_value = mock_db_connection

        # Mock the external services
        self.mock_context_service = MockContextService.return_value
        self.mock_photos_service = MockPhotosService.return_value
        self.mock_image_description_service = MockImageDescriptionService.return_value
        self.mock_embedding_service = MockEmbeddingService.return_value
        self.mock_database_service = MockDatabaseService.return_value
        self.mock_post = mock_post

        # Mock database-related calls to avoid actual DB connection
        self.mock_database_service.get_top_k_similar_records.return_value = [
            {"content": "Context 1", "similarity": 0.9},
            {"content": "Context 2", "similarity": 0.8},
            {"content": "Context 3", "similarity": 0.7},
        ]
        self.mock_database_service.get_top_k_similar_records.return_value = []

        # Mock the embedding service to avoid calling the actual model
        self.mock_embedding_service.embed_context.return_value = np.array(['dummy_embedding'])

        # Create an instance of ContentGenerationService
        self.service = ContentGenerationService(model_name="test-model")


    def test_get_image_descriptions(self):
        # Mock the image description service and photos service
        self.mock_photos_service.get_photo.return_value = [{"embedding": json.dumps([0.1, 0.2, 0.3]), "norm": 1.5}]
        self.mock_image_description_service.generate_caption.return_value = "An image of a tomato plant."

        # Test image description retrieval
        event_id = 123
        image_ids = [1]
        descriptions = self.service.get_image_descriptions(event_id, image_ids)

        # Assertions
        self.assertEqual(descriptions, ["An image of a tomato plant."])
        self.mock_photos_service.get_photo.assert_called_once()
        self.mock_image_description_service.generate_caption.assert_called_once()

    def test_get_image_descriptions_empty(self):
        # Mock the photos service to return no photos
        self.mock_photos_service.get_photo.return_value = []

        # Test scenario where no image is found
        event_id = 123
        image_ids = []
        descriptions = self.service.get_image_descriptions(event_id, image_ids)

        # Assertions
        self.assertEqual(descriptions, [])
        self.mock_photos_service.get_photo.assert_not_called()

if __name__ == '__main__':
    unittest.main()
