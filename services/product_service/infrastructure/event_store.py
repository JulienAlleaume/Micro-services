from sqlalchemy.orm import Session
from services.product_service.infrastructure.db.schema import EventDB
from domain.events import ProductCreatedEvent

class EventStore:
    """
    Responsable de l'archivage des événements dans la base de données.
    C'est notre 'Journal de Combat' ou 'Audit Log'.
    """
    def __init__(self, session: Session):
        self.session = session

    def save_event(self, event: ProductCreatedEvent):
        """Enregistre un événement dans la table events."""
        event_db = EventDB(
            aggregate_id=event.product_id,
            event_type=type(event).__name__, # Récupère "ProductCreatedEvent"
            payload=event.model_dump_json(), # Convertit l'objet en JSON string
            created_at=event.created_at
        )
        
        self.session.add(event_db)
        self.session.commit()
        print(f"Event saved to DB: {event_db.event_type} for ID {event_db.aggregate_id}")
