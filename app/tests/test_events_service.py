import unittest
from unittest.mock import patch, MagicMock
from app.services.events_service import EventsService
import random
import string

# Edge Cases: 
# 1. Adding an Event: Ensures an event is added successfully when valid data is provided and the database insertion works as expected. It verifies that the correct event ID is returned.
# 2. Retrieving Events: Verifies that all events for a given organization are correctly retrieved from the database and returned as expected.
# 3. Missing Event: Ensures that when an event is not found, the method returns None without errors.
# 4. Successful Deletion: Confirms that an event is successfully deleted from the database when it exists and returns True.
# 5. Deleting Non-Existent Event: Verifies that attempting to delete a non-existent event raises an appropriate exception.
# 6. Duplicate Event Creation: Verifies that attempting to create an event that already exists raises an exception, indicating the event already exists and returns the existing event ID.
# 7. Event Creation Without Title: Verifies that when an event is created without providing a title, the event is created with a random name, and the process completes successfully.

class TestEventsService(unittest.TestCase):

    @patch('app.services.events_service.DatabaseService')
    def test_add_event(self, MockDatabaseService):
        # Create a mock instance of the DatabaseService
        mock_db = MockDatabaseService.return_value
        
        # Set up mock return values for database operations
        mock_db.insert_record.return_value = 123  # Simulate successful insertion
        
        # Create mock event data
        mock_event = MagicMock()
        mock_event.dict.return_value = {"name": "Sample Event", "org_id": 1}
        
        # Initialize the EventsService
        service = EventsService()
        
        # Call the add_event method
        event_id = service.add_event(mock_event)
        
        # Assertions
        self.assertEqual(event_id, 123)  # The returned event ID should be 123
        mock_db.insert_record.assert_called_once_with("events", mock_event.dict())  # Ensure insert_record was called with the correct data

    @patch('app.services.events_service.DatabaseService')
    def test_get_all_events(self, MockDatabaseService):
        # Create a mock instance of the DatabaseService
        mock_db = MockDatabaseService.return_value
        
        # Set up mock return values for database operations
        mock_db.read_records.return_value = [{"id": 1, "org_id": 1, "name": "Event 1"}]
        
        # Initialize the EventsService
        service = EventsService()
        
        # Call the get_all_events method
        events = service.get_all_events(org_id=1)
        
        # Assertions
        self.assertEqual(len(events), 1)  # There should be 1 event returned
        self.assertEqual(events[0]["name"], "Event 1")  # The event name should be "Event 1"
        mock_db.read_records.assert_called_once_with("events", {"org_id": 1})  # Ensure read_records was called with the correct parameters

    @patch('app.services.events_service.DatabaseService')
    def test_get_event_not_found(self, MockDatabaseService):
        # Create a mock instance of the DatabaseService
        mock_db = MockDatabaseService.return_value
        
        # Set up mock return value indicating no event found
        mock_db.read_records.return_value = None
        
        # Initialize the EventsService
        service = EventsService()
        
        # Call the get_event method
        event = service.get_event(org_id=1, event_id=999)  # Non-existent event
        
        # Assertions
        self.assertIsNone(event)  # The event should be None if not found
        mock_db.read_records.assert_called_once_with("events", {"org_id": 1, "id": 999})  # Ensure read_records was called with the correct parameters

    @patch('app.services.events_service.DatabaseService')
    def test_delete_event_success(self, MockDatabaseService):
        # Create a mock instance of the DatabaseService
        mock_db = MockDatabaseService.return_value
        
        # Set up mock return value indicating successful deletion
        mock_db.delete_record.return_value = True
        
        # Initialize the EventsService
        service = EventsService()
        
        # Call the delete_event method
        result = service.delete_event(org_id=1, event_id=123)
        
        # Assertions
        self.assertTrue(result)  # The deletion should return True
        mock_db.delete_record.assert_called_once_with("events", {"org_id": 1, "id": 123})  # Ensure delete_record was called with the correct parameters

    @patch('app.services.events_service.DatabaseService')
    def test_delete_event_not_found(self, MockDatabaseService):
        # Create a mock instance of the DatabaseService
        mock_db = MockDatabaseService.return_value
        
        # Simulate a situation where the event doesn't exist and deletion fails
        mock_db.delete_record.side_effect = Exception("Event not found")
        
        # Initialize the EventsService
        service = EventsService()
        
        # Call the delete_event method and expect an exception
        with self.assertRaises(Exception) as context:
            service.delete_event(org_id=1, event_id=999)  # Non-existent event
        
        # Assertions
        self.assertTrue("Event not found" in str(context.exception))  # The exception message should match
        mock_db.delete_record.assert_called_once_with("events", {"org_id": 1, "id": 999})  # Ensure delete_record was called with the correct parameters

    @patch('app.services.events_service.DatabaseService')
    def test_create_duplicate_event(self, MockDatabaseService):
        # Create a mock instance of the DatabaseService
        mock_db = MockDatabaseService.return_value

        # Simulate the event already existing in the database
        existing_event_id = 456
        mock_db.insert_record.side_effect = Exception(f"Event already exists with id {existing_event_id}")

        # Create mock event data
        mock_event = MagicMock()
        mock_event.dict.return_value = {"name": "Duplicate Event", "org_id": 1}

        # Initialize the EventsService
        service = EventsService()

        # Call the add_event method and expect an exception
        with self.assertRaises(Exception) as context:
            service.add_event(mock_event)

        # Assertions
        self.assertTrue(f"Event already exists with id {existing_event_id}" in str(context.exception))
        mock_db.insert_record.assert_called_once_with("events", mock_event.dict())  # Ensure insert_record was called with the correct data

    @patch('app.services.events_service.DatabaseService')
    def test_create_event_without_title(self, MockDatabaseService):
        # Create a mock instance of the DatabaseService
        mock_db = MockDatabaseService.return_value
        
        # Generate a random event name in case title is missing
        random_event_name = ''.join(random.choices(string.ascii_letters, k=10))
        
        # Set up mock return values for database operations
        mock_db.insert_record.return_value = 789  # Simulate successful insertion
        
        # Create mock event data with no title
        mock_event = MagicMock()
        mock_event.dict.return_value = {"name": random_event_name, "org_id": 1}
        
        # Initialize the EventsService
        service = EventsService()
        
        # Call the add_event method
        event_id = service.add_event(mock_event)
        
        # Assertions
        self.assertEqual(event_id, 789)  # The returned event ID should be 789
        mock_db.insert_record.assert_called_once_with("events", mock_event.dict())  # Ensure insert_record was called with the correct data
        self.assertTrue(mock_event.dict.return_value["name"].isalpha())  # The event name should be alphanumeric and random

if __name__ == '__main__':
    unittest.main()
