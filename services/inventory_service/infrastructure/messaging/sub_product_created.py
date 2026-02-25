import os
import json
import time
import zmq

from domain.entities import Inventory
from infrastructure.db.units_of_work import UnitOfWork
from infrastructure.db.repository import InventoryRepository
from application.services.crud_services import InventoryService

# URL du socket PUB du product_service
PRODUCT_ZMQ_URL = os.getenv("PRODUCT_ZMQ_URL", "tcp://product_service:5555")


def _handle_event(event: dict):
    """
    Cree automatiquement une ligne d'inventaire (stock 0) pour le nouveau produit.
    """
    print(f"Event received: product.created for product_id={event.get('product_id')}")
    try:
        default_inventory = Inventory(
            product_id=event["product_id"],
            product_name=event["name"],
            warehouse_id=1,   # Entrepot par defaut
            quantity=0,       # Stock initial a 0
        )
        with UnitOfWork() as uow:
            repo = InventoryRepository(uow.session)
            service = InventoryService(repo)
            created = service.create(default_inventory)
            print(f"Default inventory created: {created.model_dump()}")
    except Exception as e:
        print(f"Error creating default inventory: {e}")


def start_subscriber():
    """Demarre le subscriber ZMQ pour les evenements ProductCreated."""
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect(PRODUCT_ZMQ_URL)
    socket.setsockopt_string(zmq.SUBSCRIBE, "")

    # Pause pour eviter le 'slow joiner' problem
    time.sleep(1)

    print(f"Inventory SUB connected to {PRODUCT_ZMQ_URL}, waiting for events...")

    while True:
        try:
            message = socket.recv_string()
            event = json.loads(message)
            _handle_event(event)
        except Exception as e:
            print(f"Subscriber error: {e}")
