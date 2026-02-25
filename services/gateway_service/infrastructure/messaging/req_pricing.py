import os
import json
import zmq

# URL du socket REP du pricing_service
PRICING_ZMQ_URL = os.getenv("PRICING_ZMQ_URL", "tcp://pricing_service:5556")

# Contexte ZMQ partagé au niveau du module (un seul contexte par processus)
_context = zmq.Context()


class PricingRpcClient:
    """
    Client REQ ZMQ pour communiquer avec le Pricing Service.
    Crée un socket REQ par requête et le ferme après usage.
    """

    def __init__(self):
        self._socket = _context.socket(zmq.REQ)
        # Timeout de 10 secondes en réception
        self._socket.setsockopt(zmq.RCVTIMEO, 10_000)
        self._socket.setsockopt(zmq.SNDTIMEO, 5_000)
        self._socket.connect(PRICING_ZMQ_URL)

    def call(self, action: str, data: dict | None = None) -> dict:
        """Envoie une requête REQ et attend la réponse REP de manière synchrone."""
        request_body = json.dumps({"action": action, "data": data or {}})
        self._socket.send_string(request_body)
        response_str = self._socket.recv_string()
        return json.loads(response_str)

    def close(self):
        """Ferme le socket après usage."""
        self._socket.close()
