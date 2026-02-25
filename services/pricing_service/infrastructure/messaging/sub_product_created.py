import os
import json
import time
import zmq

from domain.entities import Price
from infrastructure.db.units_of_work import UnitOfWork
from infrastructure.db.repository import PriceRepository
from application.services.crud_services import PricingService

# URL du socket PUB du product_service
PRODUCT_ZMQ_URL = os.getenv("PRODUCT_ZMQ_URL", "tcp://product_service:5555")


def _handle_event(event: dict):
    """
    Crée automatiquement un prix par défaut pour le nouveau produit.
    """
    print(f"📬 Event received: product.created for product_id={event.get('product_id')}")
    try:
        default_price = Price(
            product_id=event["product_id"],
            product_name=event["name"],
            amount=100.0,   # Prix par défaut en pièces d'or
            currency="gold",
        )
        with UnitOfWork() as uow:
            repo = PriceRepository(uow.session)
            service = PricingService(repo)
            created = service.create_price(default_price)
            print(f"✅ Default price created: {created.model_dump()}")
    except Exception as e:
        print(f"❌ Error creating default price: {e}")


def start_subscriber():
    """Démarre le subscriber ZMQ pour les événements ProductCreated."""
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect(PRODUCT_ZMQ_URL)
    socket.setsockopt_string(zmq.SUBSCRIBE, "")  # Abonnement à tous les messages

    # Petite pause pour laisser le temps à la connexion ZMQ de s'établir
    # (évite le 'slow joiner' problem)
    time.sleep(1)

    print(f"📡 Pricing SUB connected to {PRODUCT_ZMQ_URL}, waiting for events…")

    while True:
        try:
            message = socket.recv_string()
            event = json.loads(message)
            _handle_event(event)
        except Exception as e:
            print(f"❌ Subscriber error: {e}")
