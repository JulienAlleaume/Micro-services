import os
import json
import zmq

CUSTOMER_ZMQ_URL = os.getenv("CUSTOMER_ZMQ_URL", "tcp://customer_service:5559")

_context = zmq.Context()


class CustomerRpcClient:
    """Client REQ ZMQ pour communiquer avec le Customer Service."""

    def __init__(self):
        self._socket = _context.socket(zmq.REQ)
        self._socket.setsockopt(zmq.RCVTIMEO, 10_000)
        self._socket.setsockopt(zmq.SNDTIMEO, 5_000)
        self._socket.connect(CUSTOMER_ZMQ_URL)

    def call(self, action: str, data: dict | None = None) -> dict:
        request_body = json.dumps({"action": action, "data": data or {}})
        self._socket.send_string(request_body)
        response_str = self._socket.recv_string()
        return json.loads(response_str)

    def close(self):
        self._socket.close()
