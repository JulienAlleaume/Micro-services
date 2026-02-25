import os
import httpx
from typing import List

PRODUCT_SERVICE_URL = os.getenv("PRODUCT_SERVICE_URL", "http://product_service:8001")


class ProductGatewayService:
    """
    Service applicatif de la Gateway pour le microservice Product.
    Encapsule tous les appels HTTP vers le product_service.
    C'est le 'Port' côté application, ses méthodes représentent les cas d'usage exposés.
    """

    async def get_all_products(self) -> List[dict]:
        """Récupère la liste complète des produits depuis le product_service."""
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{PRODUCT_SERVICE_URL}/products/")
            response.raise_for_status()
            return response.json()

    async def get_product(self, product_id: int) -> dict:
        """Récupère un produit par son ID depuis le product_service."""
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{PRODUCT_SERVICE_URL}/products/{product_id}")
            response.raise_for_status()
            return response.json()

    async def create_product(self, payload: dict) -> dict:
        """Crée un nouveau produit dans le product_service."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{PRODUCT_SERVICE_URL}/products/",
                json=payload
            )
            response.raise_for_status()
            return response.json()
