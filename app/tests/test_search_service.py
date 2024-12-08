
import unittest
from unittest.mock import patch, MagicMock
from app.services.search_service import SearchService
import numpy as np
import json


#Edge Case 1: The database returns an empty list, ensuring the method can handle a lack of results gracefully.
#Edge Case 2: Only some records meet the similarity threshold, ensuring proper filtering logic.

class TestSearchService(unittest.TestCase):
    
    @patch('app.services.search_service.DatabaseService')
    def test_search_no_similar_records(self, MockDatabaseService):
        # Create a mock database instance
        mock_db = MockDatabaseService.return_value
        
        # Simulate no similar records from the database
        mock_db.get_similar_records.return_value = []
        
        # Initialize the SearchService
        service = SearchService()
        
        # Test parameters
        event_id = 123
        embedding = np.array([[0.1, 0.2, 0.3]])
        threshold = 0.5
        
        # Call the search method
        result = service.search(event_id, embedding, threshold)
        
        # Assertions
        self.assertEqual(result, [])  # No records should be returned
        mock_db.get_similar_records.assert_called_once_with(
            "images", "embedding", event_id, json.dumps(embedding.tolist()[0])
        )
        mock_db.close.assert_called_once()

    @patch('app.services.search_service.DatabaseService')
    def test_search_some_similar_records(self, MockDatabaseService):
        # Create a mock database instance
        mock_db = MockDatabaseService.return_value
        
        # Simulate similar records returned from the database
        mock_db.get_similar_records.return_value = [
            {'id': 1, 'similarity': 0.6},
            {'id': 2, 'similarity': 0.4},  # Below threshold
            {'id': 3, 'similarity': 0.8}
        ]
        
        # Initialize the SearchService
        service = SearchService()
        
        # Test parameters
        event_id = 123
        embedding = np.array([[0.1, 0.2, 0.3]])
        threshold = 0.5
        
        # Call the search method
        result = service.search(event_id, embedding, threshold)
        
        # Assertions
        self.assertEqual(result, [1, 3])  # Only IDs with similarity > threshold
        mock_db.get_similar_records.assert_called_once_with(
            "images", "embedding", event_id, json.dumps(embedding.tolist()[0])
        )
        mock_db.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()
