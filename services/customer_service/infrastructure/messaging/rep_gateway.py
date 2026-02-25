import os
import json
import zmq

from infrastructure.db.units_of_work import UnitOfWork
from infrastructure.db.repository import CustomerRepository
from application.services.crud_services import CustomerService
from domain.entities import Customer

CUSTOMER_REP_PORT = os.getenv("CUSTOMER_REP_PORT", "5559")


def _handle_request(body: dict) -> dict:
    """Traite une requete RPC provenant de la gateway."""
    action = body.get("action")
    data = body.get("data", {})

    with UnitOfWork() as uow:
        repo = CustomerRepository(uow.session)
        service = CustomerService(repo)

        try:
            if action == "get_all":
                customers = service.get_all()
                return {"success": True, "data": [c.model_dump() for c in customers]}

            elif action == "get_by_id":
                customer = service.get_by_id(data["customer_id"])
                return {"success": True, "data": customer.model_dump()}

            elif action == "create":
                new_customer = Customer(**data)
                created = service.create(new_customer)
                return {"success": True, "data": created.model_dump()}

            elif action == "update":
                customer_id = data.pop("customer_id")
                updated = service.update(customer_id, data)
                return {"success": True, "data": updated.model_dump()}

            else:
                return {"success": False, "error": f"Action inconnue: {action}"}

        except Exception as e:
            return {"success": False, "error": str(e)}


def start_rpc_server():
    """Demarre le serveur REP ZMQ pour le Customer Service."""
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind(f"tcp://0.0.0.0:{CUSTOMER_REP_PORT}")

    print(f"Customer REP socket bound on port {CUSTOMER_REP_PORT}, waiting for requests...")

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
