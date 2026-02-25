import os
import json
import zmq

from infrastructure.db.units_of_work import UnitOfWork
from infrastructure.db.repository import OrderRepository
from application.services.crud_services import OrderService
from domain.entities import Order, OrderLine, OrderStatus
from domain.events import OrderLineCreatedEvent

ORDER_REP_PORT = os.getenv("ORDER_REP_PORT", "5558")

# Publisher global — initialise au premier appel
_publisher = None


def _get_publisher():
    global _publisher
    if _publisher is None:
        from infrastructure.messaging.pub_orderline import OrderEventPublisher
        _publisher = OrderEventPublisher()
    return _publisher


def _handle_request(body: dict) -> dict:
    """Traite une requete RPC provenant de la gateway."""
    action = body.get("action")
    data = body.get("data", {})

    with UnitOfWork() as uow:
        repo = OrderRepository(uow.session)
        service = OrderService(repo)

        try:
            if action == "get_all":
                orders = service.get_all()
                return {"success": True, "data": [o.model_dump() for o in orders]}

            elif action == "get_by_id":
                order = service.get_by_id(data["order_id"])
                return {"success": True, "data": order.model_dump()}

            elif action == "create":
                # Construction des lignes de commande
                lines = [OrderLine(**l) for l in data.get("lines", [])]
                order = Order(
                    customer_id=data["customer_id"],
                    status=OrderStatus.PENDING,
                    lines=lines,
                )
                created = service.create(order)

                # Publie un evenement pour chaque ligne de commande
                publisher = _get_publisher()
                for line in created.lines:
                    event = OrderLineCreatedEvent(
                        order_id=created.id,
                        product_id=line.product_id,
                        warehouse_id=1,
                        quantity=line.quantity,
                    )
                    publisher.publish_orderline_created(event)

                return {"success": True, "data": created.model_dump()}

            elif action == "update_status":
                updated = service.update_status(data["order_id"], data["status"])
                return {"success": True, "data": updated.model_dump()}

            else:
                return {"success": False, "error": f"Action inconnue: {action}"}

        except Exception as e:
            return {"success": False, "error": str(e)}


def start_rpc_server():
    """Demarre le serveur REP ZMQ pour le Order Service."""
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind(f"tcp://0.0.0.0:{ORDER_REP_PORT}")

    print(f"Order REP socket bound on port {ORDER_REP_PORT}, waiting for requests...")

    while True:
        try:
            message = socket.recv_string()
            request = json.loads(message)
            print(f"RPC request: {request.get('action')}")

            response = _handle_request(request)

            socket.send_string(json.dumps(response))
            print(f"RPC response sent for action '{request.get('action')}'")
        except Exception as e:
            print(f"REP server error: {e}")
            socket.send_string(json.dumps({"success": False, "error": str(e)}))
