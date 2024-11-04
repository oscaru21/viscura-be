import json
import os
from app.services.embedding_service import EmbeddingService
from app.services.database_service import DatabaseService

class PhotosService:
    def __init__(self, embedding_service: EmbeddingService):
        self.IMAGE_DIR = "images"
        self.embedding_service = embedding_service
        
    def get_photo(self, event_id, photo_id):
        db = DatabaseService()
        photo = db.read_records("images", {"event_id": event_id, "id": photo_id})
        db.close()
        return photo

    def add_photo(self, photo, event_id):
        db = DatabaseService()
        image_embedding, norm_factor = self.embedding_service.embed_image(photo)
        #transform norm_factor from eager tensor to float
        norm_factor = norm_factor.numpy()[0]
        norm_factor = float(norm_factor)
        image_id = db.insert_record("images", {"event_id": event_id, "embedding": json.dumps(image_embedding.tolist()[0]), "norm": norm_factor})
        db.close()
        # Create the directory if it doesn't exist
        if not os.path.exists(os.path.join(self.IMAGE_DIR, event_id)):
            os.makedirs(os.path.join(self.IMAGE_DIR, event_id))
        # Save the image with the ID as the name
        image_path = os.path.join(self.IMAGE_DIR, event_id, f"{image_id}.png")
        photo.save(image_path)  
        
        return image_id

    def update_photo(self, photo_id, photo):
        return self.photos_repository.update_photo(photo_id, photo)

    def delete_photo(self, event_id, photo_id):
        db = DatabaseService()
        db.delete_record("images", {"event_id": event_id, "id": photo_id})
        db.close()
        # Delete the image file
        if not os.path.exists(os.path.join(self.IMAGE_DIR, event_id, f"{photo_id}.png")):
            return
        image_path = os.path.join(self.IMAGE_DIR, event_id, f"{photo_id}.png")
        os.remove(image_path)