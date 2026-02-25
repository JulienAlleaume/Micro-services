from infrastructure.messaging.req_customer import CustomerRpcClient


class CustomerGatewayService:
    """Service applicatif de la Gateway pour le Customer Service."""

    def get_all(self) -> list[dict]:
        client = CustomerRpcClient()
        try:
            response = client.call("get_all")
            if response.get("success"):
                return response["data"]
            raise Exception(response.get("error", "Unknown error"))
        finally:
            client.close()

    def get_by_id(self, customer_id: int) -> dict:
        client = CustomerRpcClient()
        try:
            response = client.call("get_by_id", {"customer_id": customer_id})
            if response.get("success"):
                return response["data"]
            raise Exception(response.get("error", "Unknown error"))
        finally:
            client.close()

    def create(self, payload: dict) -> dict:
        client = CustomerRpcClient()
        try:
            response = client.call("create", payload)
            if response.get("success"):
                return response["data"]
            raise Exception(response.get("error", "Unknown error"))
        finally:
            client.close()

    def update(self, customer_id: int, payload: dict) -> dict:
        payload["customer_id"] = customer_id
        client = CustomerRpcClient()
        try:
            response = client.call("update", payload)
            if response.get("success"):
                return response["data"]
            raise Exception(response.get("error", "Unknown error"))
        finally:
            client.close()
