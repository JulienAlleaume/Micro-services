import os
import json
import time
import zmq

from infrastructure.db.units_of_work import UnitOfWork
from infrastructure.db.repository import InventoryRepository
from application.services.crud_services import InventoryService

# URL du socket PUB du order_service (evenement orderline.created)
# Ce subscriber sera actif quand order_service sera implemente.
ORDERLINE_ZMQ_URL = os.getenv("ORDERLINE_ZMQ_URL", "tcp://order_service:5558")


def _handle_event(event: dict):
    """
    Decremente le stock quand une ligne de commande est creee.
    L'evenement contient : product_id, warehouse_id, quantity.
    """
    print(
        f"Event received: orderline.created for product_id={event.get('product_id')}, "
        f"warehouse_id={event.get('warehouse_id')}, qty={event.get('quantity')}"
    )
    try:
        with UnitOfWork() as uow:
            repo = InventoryRepository(uow.session)
            service = InventoryService(repo)
            updated = service.decrement_stock(
                warehouse_id=event["warehouse_id"],
                product_id=event["product_id"],
                amount=event["quantity"],
            )
            print(f"Stock decremented: {updated.model_dump()}")
    except Exception as e:
        print(f"Error decrementing stock: {e}")


def start_subscriber():
    """Demarre le subscriber ZMQ pour les evenements OrderLineCreated."""
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect(ORDERLINE_ZMQ_URL)
    socket.setsockopt_string(zmq.SUBSCRIBE, "")

    time.sleep(1)

    print(f"Inventory SUB (orderline) connected to {ORDERLINE_ZMQ_URL}, waiting for events...")

    while True:
        try:
            message = socket.recv_string()
            event = json.loads(message)
            _handle_event(event)
        except Exception as e:
            print(f"OrderLine subscriber error: {e}")
