from infrastructure.messaging.req_inventory import InventoryRpcClient


class InventoryGatewayService:
    """
    Service applicatif de la Gateway pour l'Inventory Service.
    Communique via ZMQ REQ/REP.
    """

    def get_all(self) -> list[dict]:
        client = InventoryRpcClient()
        try:
            response = client.call("get_all")
            if response.get("success"):
                return response["data"]
            raise Exception(response.get("error", "Unknown error"))
        finally:
            client.close()

    def get_by_product(self, product_id: int) -> list[dict]:
        client = InventoryRpcClient()
        try:
            response = client.call("get_by_product", {"product_id": product_id})
            if response.get("success"):
                return response["data"]
            raise Exception(response.get("error", "Unknown error"))
        finally:
            client.close()

    def update_quantity(self, warehouse_id: int, product_id: int, payload: dict) -> dict:
        payload["warehouse_id"] = warehouse_id
        payload["product_id"] = product_id
        client = InventoryRpcClient()
        try:
            response = client.call("update_quantity", payload)
            if response.get("success"):
                return response["data"]
            raise Exception(response.get("error", "Unknown error"))
        finally:
            client.close()
