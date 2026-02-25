import os
import zmq
from domain.events import ProductCreatedEvent

# Le publisher BIND sur ce port ; les subscribers se connectent à tcp://product_service:<port>
ZMQ_PUB_PORT = os.getenv("ZMQ_PUB_PORT", "5555")


class ProductEventPublisher:
    """
    Adapter de sortie pour publier des événements produit via ZeroMQ (pattern PUB).
    Le socket est en mode BIND : il est stable, les subscribers se connectent à lui.
    """

    def __init__(self):
        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.PUB)
        self._socket.bind(f"tcp://0.0.0.0:{ZMQ_PUB_PORT}")
        print(f"ZMQ PUB socket bound on port {ZMQ_PUB_PORT}")

    def publish_product_created(self, event: ProductCreatedEvent):
        """Publie un événement de création de produit via ZMQ."""
        message_body = event.model_dump_json()
        self._socket.send_string(message_body)
        print(f"Event published via ZMQ PUB: {message_body}")

    def close(self):
        """Ferme le socket ZMQ."""
        self._socket.close()
        self._context.term()
