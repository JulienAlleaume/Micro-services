import os
import json
import zmq

from infrastructure.db.units_of_work import UnitOfWork
from infrastructure.db.repository import PriceRepository
from application.services.crud_services import PricingService
from domain.entities import Price

# Le serveur REP BIND sur ce port ; le client REQ (gateway) se connecte à lui
PRICING_REP_PORT = os.getenv("PRICING_REP_PORT", "5556")


def _handle_request(body: dict) -> dict:
    """Traite une requête RPC provenant de la gateway."""
    action = body.get("action")
    data = body.get("data", {})

    with UnitOfWork() as uow:
        repo = PriceRepository(uow.session)
        service = PricingService(repo)

        try:
            if action == "get_all":
                prices = service.get_all_prices()
                return {"success": True, "data": [p.model_dump() for p in prices]}

            elif action == "get_by_id":
                price = service.get_price(data["price_id"])
                return {"success": True, "data": price.model_dump()}

            elif action == "get_by_product":
                price = service.get_price_by_product(data["product_id"])
                return {"success": True, "data": price.model_dump()}

            elif action == "create":
                new_price = Price(**data)
                created = service.create_price(new_price)
                return {"success": True, "data": created.model_dump()}

            elif action == "update":
                updated = service.update_price(
                    price_id=data["price_id"],
                    amount=data["amount"],
                    currency=data.get("currency"),
                )
                return {"success": True, "data": updated.model_dump()}

            else:
                return {"success": False, "error": f"Action inconnue: {action}"}

        except Exception as e:
            return {"success": False, "error": str(e)}


def start_rpc_server():
    """Démarre le serveur REP ZMQ pour le Pricing Service."""
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind(f"tcp://0.0.0.0:{PRICING_REP_PORT}")

    print(f"🚀 Pricing REP socket bound on port {PRICING_REP_PORT}, waiting for requests…")

    while True:
        try:
            message = socket.recv_string()
            request = json.loads(message)
            print(f"📥 RPC request: {request.get('action')}")

            response = _handle_request(request)

            socket.send_string(json.dumps(response))
            print(f"📤 RPC response sent for action '{request.get('action')}'")
        except Exception as e:
            # En cas d'erreur inattendue, on envoie quand même une réponse
            # pour ne pas bloquer le socket REP
            print(f"❌ REP server error: {e}")
            socket.send_string(json.dumps({"success": False, "error": str(e)}))
