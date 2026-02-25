from infrastructure.messaging.req_order import OrderRpcClient


class OrderGatewayService:
    """Service applicatif de la Gateway pour le Order Service."""

    def get_all(self) -> list[dict]:
        client = OrderRpcClient()
        try:
            response = client.call("get_all")
            if response.get("success"):
                return response["data"]
            raise Exception(response.get("error", "Unknown error"))
        finally:
            client.close()

    def get_by_id(self, order_id: int) -> dict:
        client = OrderRpcClient()
        try:
            response = client.call("get_by_id", {"order_id": order_id})
            if response.get("success"):
                return response["data"]
            raise Exception(response.get("error", "Unknown error"))
        finally:
            client.close()

    def create(self, payload: dict) -> dict:
        client = OrderRpcClient()
        try:
            response = client.call("create", payload)
            if response.get("success"):
                return response["data"]
            raise Exception(response.get("error", "Unknown error"))
        finally:
            client.close()

    def update_status(self, order_id: int, payload: dict) -> dict:
        payload["order_id"] = order_id
        client = OrderRpcClient()
        try:
            response = client.call("update_status", payload)
            if response.get("success"):
                return response["data"]
            raise Exception(response.get("error", "Unknown error"))
        finally:
            client.close()
