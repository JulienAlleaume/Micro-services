import os
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import StreamingResponse
import httpx

from application.service.pricing import PricingGatewayService
from application.service.inventory import InventoryGatewayService
from application.service.customer import CustomerGatewayService
from application.service.order import OrderGatewayService

router = APIRouter()

PRODUCT_SERVICE_URL = os.getenv("PRODUCT_SERVICE_URL", "http://product_service:8001")


async def _proxy_request(request: Request, target_base_url: str) -> StreamingResponse:
    """
    Proxy générique : redirige la requête entrante vers un microservice cible.
    Conserve la méthode HTTP, les headers, les query params et le body.
    Streame la réponse pour supporter les gros fichiers (images, etc.).
    """
    async with httpx.AsyncClient() as client:
        # Construction de l'URL cible
        url = f"{target_base_url}{request.url.path}"
        if request.url.query:
            url += f"?{request.url.query}"

        # On retire le header 'host' pour éviter les confusions côté microservice
        headers = dict(request.headers)
        headers.pop("host", None)

        req = client.build_request(
            method=request.method,
            url=url,
            headers=headers,
            content=await request.body(),
        )

        response = await client.send(req, stream=True)

        return StreamingResponse(
            response.aiter_raw(),
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.headers.get("content-type"),
        )


# ──────────────────────────────────────────────
#  Routes Pricing (via ZMQ RPC)
#  Définies AVANT le catch-all pour avoir priorité
# ──────────────────────────────────────────────

@router.get("/prices/")
def get_all_prices():
    """Liste tous les prix."""
    try:
        service = PricingGatewayService()
        return service.get_all_prices()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/prices/product/{product_id}")
def get_price_by_product(product_id: int):
    """Récupère le prix associé à un produit."""
    try:
        service = PricingGatewayService()
        return service.get_price_by_product(product_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/prices/{price_id}")
def get_price(price_id: int):
    """Récupère un prix par son ID."""
    try:
        service = PricingGatewayService()
        return service.get_price(price_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/prices/", status_code=201)
def create_price(request_body: dict):
    """Crée un nouveau prix."""
    try:
        service = PricingGatewayService()
        return service.create_price(request_body)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/prices/{price_id}")
def update_price(price_id: int, request_body: dict):
    """Met à jour un prix existant."""
    try:
        service = PricingGatewayService()
        return service.update_price(price_id, request_body)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ──────────────────────────────────────────────
#  Routes Inventory (via ZMQ RPC)
# ──────────────────────────────────────────────

@router.get("/inventory/")
def get_all_inventory():
    """Liste tout l'inventaire."""
    try:
        service = InventoryGatewayService()
        return service.get_all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/inventory/{product_id}")
def get_inventory_by_product(product_id: int):
    """Recupere l'inventaire pour un produit donne."""
    try:
        service = InventoryGatewayService()
        return service.get_by_product(product_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/inventory/{warehouse_id}/{product_id}")
def update_inventory(warehouse_id: int, product_id: int, request_body: dict):
    """Met a jour la quantite en stock pour un entrepot/produit."""
    try:
        service = InventoryGatewayService()
        return service.update_quantity(warehouse_id, product_id, request_body)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ──────────────────────────────────────────────
#  Routes Customer (via ZMQ RPC)
# ──────────────────────────────────────────────

@router.get("/customers/")
def get_all_customers():
    """Liste tous les clients."""
    try:
        service = CustomerGatewayService()
        return service.get_all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/customers/{customer_id}")
def get_customer(customer_id: int):
    """Recupere un client par son ID."""
    try:
        service = CustomerGatewayService()
        return service.get_by_id(customer_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/customers/", status_code=201)
def create_customer(request_body: dict):
    """Cree un nouveau client."""
    try:
        service = CustomerGatewayService()
        return service.create(request_body)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/customers/{customer_id}")
def update_customer(customer_id: int, request_body: dict):
    """Met a jour un client existant."""
    try:
        service = CustomerGatewayService()
        return service.update(customer_id, request_body)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ──────────────────────────────────────────────
#  Routes Order (via ZMQ RPC)
# ──────────────────────────────────────────────

@router.get("/orders/")
def get_all_orders():
    """Liste toutes les commandes."""
    try:
        service = OrderGatewayService()
        return service.get_all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/orders/{order_id}")
def get_order(order_id: int):
    """Recupere une commande par son ID."""
    try:
        service = OrderGatewayService()
        return service.get_by_id(order_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/orders/", status_code=201)
def create_order(request_body: dict):
    """Cree une nouvelle commande."""
    try:
        service = OrderGatewayService()
        return service.create(request_body)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/orders/{order_id}")
def update_order_status(order_id: int, request_body: dict):
    """Met a jour le statut d'une commande."""
    try:
        service = OrderGatewayService()
        return service.update_status(order_id, request_body)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ──────────────────────────────────────────────
#  Route catch-all — proxy HTTP vers les autres services
# ──────────────────────────────────────────────

@router.api_route(
    "/{path:path}",
    methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
)
async def gateway_entrypoint(path: str, request: Request):
    """
    Point d'entrée de la Gateway.
    Redirige chaque requête vers le microservice approprié selon le préfixe du path.
    """
    if path.startswith("products") or path.startswith("static"):
        return await _proxy_request(request, PRODUCT_SERVICE_URL)

    return {"message": "Gateway: route non gérée", "path": path}
