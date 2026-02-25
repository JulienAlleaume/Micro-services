import os
import json
import zmq

from infrastructure.db.units_of_work import UnitOfWork
from infrastructure.db.repository import InventoryRepository, WarehouseRepository
from application.services.crud_services import InventoryService, WarehouseService
from domain.entities import Inventory, Warehouse

# Le serveur REP BIND sur ce port ; le client REQ (gateway) se connecte a lui
INVENTORY_REP_PORT = os.getenv("INVENTORY_REP_PORT", "5557")


def _handle_request(body: dict) -> dict:
    """Traite une requete RPC provenant de la gateway."""
    action = body.get("action")
    data = body.get("data", {})

    with UnitOfWork() as uow:
        inv_repo = InventoryRepository(uow.session)
        inv_service = InventoryService(inv_repo)
        wh_repo = WarehouseRepository(uow.session)
        wh_service = WarehouseService(wh_repo)

        try:
            # -- Inventory actions --
            if action == "get_all":
                items = inv_service.get_all()
                return {"success": True, "data": [i.model_dump() for i in items]}

            elif action == "get_by_product":
                items = inv_service.get_by_product(data["product_id"])
                return {"success": True, "data": [i.model_dump() for i in items]}

            elif action == "get_by_warehouse_product":
                item = inv_service.get_by_warehouse_and_product(
                    data["warehouse_id"], data["product_id"]
                )
                return {"success": True, "data": item.model_dump()}

            elif action == "create":
                new_item = Inventory(**data)
                created = inv_service.create(new_item)
                return {"success": True, "data": created.model_dump()}

            elif action == "update_quantity":
                updated = inv_service.update_quantity(
                    warehouse_id=data["warehouse_id"],
                    product_id=data["product_id"],
                    quantity=data["quantity"],
                )
                return {"success": True, "data": updated.model_dump()}

            # -- Warehouse actions --
            elif action == "get_all_warehouses":
                warehouses = wh_service.get_all()
                return {"success": True, "data": [w.model_dump() for w in warehouses]}

            elif action == "get_warehouse":
                warehouse = wh_service.get_by_id(data["warehouse_id"])
                return {"success": True, "data": warehouse.model_dump()}

            elif action == "create_warehouse":
                new_wh = Warehouse(**data)
                created = wh_service.create(new_wh)
                return {"success": True, "data": created.model_dump()}

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
