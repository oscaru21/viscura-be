import unittest
from unittest.mock import patch, MagicMock
import numpy as np
from app.services.embedding_service import EmbeddingService

#test_embed_image : Verifies that the embed_image method correctly transforms and normalizes an input image into a vector embedding. It ensures that the process calls the appropriate methods (transform and normalize) and returns the expected normalized array.

#test_embed_text: Tests the embed_text method to ensure it accurately processes textual input, transforms it into an embedding, and normalizes the result. The test validates method calls and checks the returned normalized array matches expectations.

#test_embed_context : Ensures that the embed_context method uses HuggingFace embeddings to process input text, generating and normalizing a valid embedding vector. It verifies the appropriate method is called and that the returned output is normalized as expected.

class TestEmbeddingService(unittest.TestCase):

    @patch('app.services.embedding_service.ClipEmbedding')
    def test_embed_image(self, MockClipEmbedding):
        # Create mock instance of ClipEmbedding
        mock_clip_model = MockClipEmbedding.return_value
        
        # Set up mock return values for transform and normalize methods
        mock_clip_model.transform.return_value = np.array([0.1, 0.2, 0.3])
        mock_clip_model.normalize.return_value = np.array([0.3, 0.6, 0.9])  # normalized result
        
        # Initialize the EmbeddingService
        service = EmbeddingService()
        
        # Call the embed_image method
        image = MagicMock()  # Mocking the image object
        result = service.embed_image(image)
        
        # Assertions
        self.assertTrue(np.array_equal(result, np.array([0.3, 0.6, 0.9])))  # Check if the normalized result is as expected
        mock_clip_model.transform.assert_called_once_with(image, input_type='image')  # Ensure transform was called with the correct input
        mock_clip_model.normalize.assert_called_once()  # Ensure normalize was called

    @patch('app.services.embedding_service.ClipEmbedding')
    def test_embed_text(self, MockClipEmbedding):
        # Create mock instance of ClipEmbedding
        mock_clip_model = MockClipEmbedding.return_value
        
        # Set up mock return values for transform and normalize methods
        mock_clip_model.transform.return_value = np.array([0.4, 0.5, 0.6])
        mock_clip_model.normalize.return_value = np.array([0.4, 0.5, 0.6])  # normalized result
        
        # Initialize the EmbeddingService
        service = EmbeddingService()
        
        # Call the embed_text method
        text = "Sample text"
        result = service.embed_text(text)
        
        # Assertions
        self.assertTrue(np.array_equal(result, np.array([0.4, 0.5, 0.6])))  # Check if the normalized result is as expected
        mock_clip_model.transform.assert_called_once_with(text, input_type='text')  # Ensure transform was called with the correct input
        mock_clip_model.normalize.assert_called_once()  # Ensure normalize was called

    @patch('app.services.embedding_service.HuggingFaceEmbeddings')
    def test_embed_context(self, MockHuggingFaceEmbeddings):
        # Create mock instance of HuggingFaceEmbeddings
        mock_hf_model = MockHuggingFaceEmbeddings.return_value
        
        # Set up mock return values for embed_query method
        mock_hf_model.embed_query.return_value = [0.7, 0.8, 0.9]
        
        # Initialize the EmbeddingService
        service = EmbeddingService()
        
        # Call the embed_context method
        text = "Sample context text"
        result = service.embed_context(text)
        
        # Assertions
        self.assertTrue(np.array_equal(result, np.array([0.7, 0.8, 0.9]) / np.linalg.norm([0.7, 0.8, 0.9])))  # Check normalized result
        mock_hf_model.embed_query.assert_called_once_with(text)  # Ensure embed_query was called with the correct input
if __name__ == '__main__':
    unittest.main()
