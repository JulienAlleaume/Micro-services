"""
Module utilitaire pour recuperer des donnees produit depuis le product_service.

Permet a l'inventory_service d'enrichir ses reponses avec des informations produit
a jour (nom, categorie, image...) en interrogeant le product_service via HTTP.
"""
import os
import urllib.request
import json

PRODUCT_SERVICE_URL = os.getenv("PRODUCT_SERVICE_URL", "http://product_service:8001")


def fetch_product(product_id: int) -> dict | None:
    """
    Recupere les donnees d'un produit depuis le product_service (HTTP GET).
    Retourne None si le produit n'est pas trouve.
    """
    url = f"{PRODUCT_SERVICE_URL}/products/{product_id}"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        print(f"Could not fetch product {product_id}: {e}")
        return None
