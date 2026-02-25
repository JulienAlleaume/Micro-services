import os
import zmq
from domain.events import OrderLineCreatedEvent

# Le publisher BIND sur ce port ; inventory_service SUB se connecte a lui
ZMQ_PUB_PORT = os.getenv("ORDER_PUB_PORT", "5560")


class OrderEventPublisher:
    """Publie les evenements orderline.created via ZMQ PUB."""

    def __init__(self):
        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.PUB)
        self._socket.bind(f"tcp://0.0.0.0:{ZMQ_PUB_PORT}")
        print(f"Order PUB socket bound on port {ZMQ_PUB_PORT}")

    def publish_orderline_created(self, event: OrderLineCreatedEvent):
        message_body = event.model_dump_json()
        self._socket.send_string(message_body)
        print(f"Event published: orderline.created for product_id={event.product_id}")

    def close(self):
        self._socket.close()
        self._context.term()
