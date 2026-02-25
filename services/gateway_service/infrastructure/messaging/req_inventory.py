import os
import json
import zmq

# URL du socket REP de l'inventory_service
INVENTORY_ZMQ_URL = os.getenv("INVENTORY_ZMQ_URL", "tcp://inventory_service:5557")

# Contexte ZMQ partage au niveau du module
_context = zmq.Context()


class InventoryRpcClient:
    """
    Client REQ ZMQ pour communiquer avec l'Inventory Service.
    Cree un socket REQ par requete et le ferme apres usage.
    """

    def __init__(self):
        self._socket = _context.socket(zmq.REQ)
        self._socket.setsockopt(zmq.RCVTIMEO, 10_000)
        self._socket.setsockopt(zmq.SNDTIMEO, 5_000)
        self._socket.connect(INVENTORY_ZMQ_URL)

    def call(self, action: str, data: dict | None = None) -> dict:
        """Envoie une requete REQ et attend la reponse REP."""
        request_body = json.dumps({"action": action, "data": data or {}})
        self._socket.send_string(request_body)
        response_str = self._socket.recv_string()
        return json.loads(response_str)

    def close(self):
        self._socket.close()
