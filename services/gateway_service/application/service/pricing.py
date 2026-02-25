from infrastructure.messaging.req_pricing import PricingRpcClient

class PricingGatewayService:
    """
    Service applicatif de la Gateway pour le Pricing Service.
    Communique via RabbitMQ RPC (pas HTTP).
    """

    def get_all_prices(self) -> list[dict]:
        client = PricingRpcClient()
        try:
            response = client.call("get_all")
            if response.get("success"):
                return response["data"]
            raise Exception(response.get("error", "Unknown error"))
        finally:
            client.close()

    def get_price(self, price_id: int) -> dict:
        client = PricingRpcClient()
        try:
            response = client.call("get_by_id", {"price_id": price_id})
            if response.get("success"):
                return response["data"]
            raise Exception(response.get("error", "Unknown error"))
        finally:
            client.close()

    def get_price_by_product(self, product_id: int) -> dict:
        client = PricingRpcClient()
        try:
            response = client.call("get_by_product", {"product_id": product_id})
            if response.get("success"):
                return response["data"]
            raise Exception(response.get("error", "Unknown error"))
        finally:
            client.close()

    def create_price(self, payload: dict) -> dict:
        client = PricingRpcClient()
        try:
            response = client.call("create", payload)
            if response.get("success"):
                return response["data"]
            raise Exception(response.get("error", "Unknown error"))
        finally:
            client.close()

    def update_price(self, price_id: int, payload: dict) -> dict:
        payload["price_id"] = price_id
        client = PricingRpcClient()
        try:
            response = client.call("update", payload)
            if response.get("success"):
                return response["data"]
            raise Exception(response.get("error", "Unknown error"))
        finally:
            client.close()
