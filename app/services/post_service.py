from typing import List, Optional, Dict, Any
from app.services.database_service import DatabaseService
from pydantic import BaseModel

# Post request models
class PostCreateRequest(BaseModel):
    event_id: int
    caption: str
    image_ids: List[int]
    user_id: int

class PostUpdateRequest(BaseModel):
    event_id: Optional[int] = None
    caption: Optional[str] = None
    image_ids: Optional[List[int]] = None

# Post service
class PostService:
    def __init__ (self, db: DatabaseService):
        self.db = db
        self.table = "posts"

    def create_post(self, event_id:int, caption:str, image_ids:List[int], user_id:int) -> int:
        """
        Create a post in the database
        :param event_id: The id of the event
        :param caption: The caption of the post
        :param image_ids: The ids of the images in the post
        :param user_id: The id of the user who created the post
        :return: The id of the created post
        """
        post = {
            "event_id": event_id,
            "caption": caption,
            "image_ids": image_ids,
            "user_id": user_id
        }
        return self.db.insert_record(self.table, post)
    
    def get_post(self, post_id:int) -> Optional[Dict[str, Any]]:
        """
        Get a post from the database by id
        :param post_id: The id of the post
        :return: The post as a dictionary or None if not found
        """
        condition = {"id": post_id}
        records = self.db.read_records(self.table, condition)
        return records[0] if records else None
    
    def get_posts_by_event(self, event_id:int) -> List[Dict[str, Any]]:
        """
        Get all posts for a given event
        :param event_id: The id of the event
        :return: A list of posts as dictionaries
        """
        condition = {"event_id": event_id}
        records = self.db.read_records(self.table, condition)
        return records if records else []
    
    def update_post(self, post_id: int, event_id: Optional[int] = None, caption: Optional[str] = None, image_ids: Optional[List[int]] = None) -> bool:
        """
        Update a post in the database
        :param post_id: The id of the post to update
        :param event_id: The id of the event (optional)
        :param caption: The caption of the post (optional)
        :param image_ids: The ids of the images in the post (optional)
        :return: True if the update was successful, False otherwise
        """
        if not self.get_post(post_id):
            return False
        
        data = {}
        if event_id is not None:
            data["event_id"] = event_id
        if caption is not None:
            data["caption"] = caption
        if image_ids is not None:
            data["image_ids"] = image_ids

        if data:
            conditions = {"id": post_id}
            rows_updated = self.db.update_record(self.table, data, conditions)
            return rows_updated > 0
        
        return False
    
    def delete_post(self, post_id:int) -> bool:
        """
        Delete a post from the database
        :param post_id: The id of the post to delete
        :return: True if the deletion was successful, False otherwise
        """
        if self.get_post(post_id):
            conditions = {"id": post_id}
            self.db.delete_record(self.table, conditions)
            return True
        return False   
    