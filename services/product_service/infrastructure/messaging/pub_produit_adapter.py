import zmq
import json
import os
from domain.events import ProductCreatedEvent

class ProductEventPublisher:
    """
    Un adapter de sortie pour publier des événements liés aux produits sur ZeroMQ.
    """
    def __init__(self):
        # Utilise les variables d'environnement ou des valeurs par défaut
        port = os.getenv('ZMQ_PORT', '5555')
        
        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.PUB)
        self._socket.bind(f"tcp://0.0.0.0:{port}")

    def publish_product_created(self, event: ProductCreatedEvent):
        """Publie un événement de création de produit."""
        message_body = event.model_dump_json()
        
        self._socket.send_string(message_body)
        
        print(f"✅ Event published to ZMQ: {message_body}")
