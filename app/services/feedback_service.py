from app.services.database_service import DatabaseService

class FeedbackService:
    def get_feedback(self, event_id: int, post_id: int):
        db = DatabaseService()
        feedbacks = db.read_records("feedbacks", {"event_id": event_id, "post_id": post_id})
        db.close()
        return feedbacks
    
    def add_feedback(self, event_id: int, post_id: int, feedback):
        db = DatabaseService()
        feedback_id = db.insert_record("feedbacks", {"event_id": event_id, "post_id": post_id, "feedback_comment": feedback.feedback, "feedback_status": feedback.status})
        db.close()
        return feedback_id
    
    def update_feedback(self, event_id: int, post_id: int, feedback_id: int, feedback: dict):
        db = DatabaseService()
        db.update_feedback(event_id, post_id, feedback_id, feedback)
        db.close()
        return {"message": "Feedback updated successfully"}
    
    def delete_feedback(self, event_id: int, post_id: int, feedback_id: int):
        db = DatabaseService()
        db.delete_feedback(event_id, post_id, feedback_id)
        db.close()
        return {"message": "Feedback deleted successfully"}