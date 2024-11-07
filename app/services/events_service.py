from app.services.database_service import DatabaseService

class EventsService:
    def get_all_events(self, org_id):
        db = DatabaseService()
        events = db.read_records("events", {"org_id": org_id})
        db.close()
        return events

    def get_event(self, org_id, event_id):
        db = DatabaseService()
        event = db.read_records("events", {"org_id": org_id, "id": event_id})
        db.close()
        return event

    def add_event(self, event):
        db = DatabaseService()
        event_id = db.insert_record("events", event.dict())
        db.close()
        return event_id

    def delete_event(self, org_id, event_id):
        db = DatabaseService()
        db.delete_record("events", {"org_id": org_id, "id": event_id})
        db.close()
        return True