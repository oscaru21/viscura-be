import unittest
from unittest.mock import patch, MagicMock
from app.services.feedback_service import FeedbackService

# Edge Cases:
# 1. Feedback Not Found: Ensures that when no feedback exists for a given event and post, an empty list or None is returned.
# 2. Invalid Feedback Data: Ensures that when invalid data is provided for feedback creation, an exception is raised.

class TestFeedbackService(unittest.TestCase):

    @patch('app.services.feedback_service.DatabaseService')
    def test_get_feedback_not_found(self, MockDatabaseService):
        # Create a mock instance of the DatabaseService
        mock_db = MockDatabaseService.return_value
        
        # Simulate no feedback found for the given event_id and post_id
        mock_db.read_records.return_value = []
        
        # Initialize the FeedbackService
        service = FeedbackService()
        
        # Call the get_feedback method
        feedbacks = service.get_feedback(event_id=1, post_id=999)  # Non-existent feedback
        
        # Assertions
        self.assertEqual(feedbacks, [])  # The feedback should be an empty list if not found
        mock_db.read_records.assert_called_once_with("feedbacks", {"event_id": 1, "post_id": 999})  # Ensure read_records was called with the correct parameters

    @patch('app.services.feedback_service.DatabaseService')
    def test_add_feedback_invalid_data(self, MockDatabaseService):
        # Create a mock instance of the DatabaseService
        mock_db = MockDatabaseService.return_value
        
        # Simulate invalid feedback data (e.g., missing feedback comment)
        mock_db.insert_record.side_effect = Exception("Invalid feedback data")
        
        # Create mock feedback data
        mock_feedback = MagicMock()
        mock_feedback.feedback = None  # Invalid feedback data (None instead of a string)
        mock_feedback.status = "Pending"
        
        # Initialize the FeedbackService
        service = FeedbackService()
        
        # Call the add_feedback method and expect an exception
        with self.assertRaises(Exception) as context:
            service.add_feedback(event_id=1, post_id=1, feedback=mock_feedback)
        
        # Assertions
        self.assertTrue("Invalid feedback data" in str(context.exception))
        mock_db.insert_record.assert_called_once_with("feedbacks", {"event_id": 1, "post_id": 1, "feedback_comment": None, "feedback_status": "Pending"})  # Ensure insert_record was called with the invalid data

if __name__ == '__main__':
    unittest.main()
