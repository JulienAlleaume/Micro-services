import os
import json
import zmq

from infrastructure.db.units_of_work import UnitOfWork
from infrastructure.db.repository import InventoryRepository
from application.services.crud_services import InventoryService
from domain.entities import Inventory

# Le serveur REP BIND sur ce port ; le client REQ (gateway) se connecte a lui
INVENTORY_REP_PORT = os.getenv("INVENTORY_REP_PORT", "5557")


def _handle_request(body: dict) -> dict:
    """Traite une requete RPC provenant de la gateway."""
    action = body.get("action")
    data = body.get("data", {})

    with UnitOfWork() as uow:
        repo = InventoryRepository(uow.session)
        service = InventoryService(repo)

        try:
            if action == "get_all":
                items = service.get_all()
                return {"success": True, "data": [i.model_dump() for i in items]}

            elif action == "get_by_product":
                items = service.get_by_product(data["product_id"])
                return {"success": True, "data": [i.model_dump() for i in items]}

            elif action == "get_by_warehouse_product":
                item = service.get_by_warehouse_and_product(
                    data["warehouse_id"], data["product_id"]
                )
                return {"success": True, "data": item.model_dump()}

            elif action == "create":
                new_item = Inventory(**data)
                created = service.create(new_item)
                return {"success": True, "data": created.model_dump()}

            elif action == "update_quantity":
                updated = service.update_quantity(
                    warehouse_id=data["warehouse_id"],
                    product_id=data["product_id"],
                    quantity=data["quantity"],
                )
                return {"success": True, "data": updated.model_dump()}

            else:
                return {"success": False, "error": f"Action inconnue: {action}"}

        except Exception as e:
            return {"success": False, "error": str(e)}


def start_rpc_server():
    """Demarre le serveur REP ZMQ pour l'Inventory Service."""
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind(f"tcp://0.0.0.0:{INVENTORY_REP_PORT}")

    print(f"Inventory REP socket bound on port {INVENTORY_REP_PORT}, waiting for requests...")

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
