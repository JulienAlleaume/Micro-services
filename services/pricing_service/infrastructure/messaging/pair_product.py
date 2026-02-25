"""
Module utilitaire pour récupérer des données produit depuis le product_service.

Permet au pricing_service d'enrichir ses réponses avec des informations produit
à jour (nom, catégorie, image…) en interrogeant le product_service via HTTP.

NOTE : Pour l'instant, le pricing_service stocke déjà product_name en local
(copié lors de la réception de l'événement product.created).
Ce module sera utile quand on voudra resynchroniser les données ou
valider l'existence d'un produit avant de créer un prix manuellement.
"""
import os
import urllib.request
import json

PRODUCT_SERVICE_URL = os.getenv("PRODUCT_SERVICE_URL", "http://product_service:8001")


def fetch_product(product_id: int) -> dict | None:
    """
    Récupère les données d'un produit depuis le product_service (HTTP GET).
    Retourne None si le produit n'est pas trouvé.
    """
    url = f"{PRODUCT_SERVICE_URL}/products/{product_id}"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        print(f"Could not fetch product {product_id}: {e}")
        return None
