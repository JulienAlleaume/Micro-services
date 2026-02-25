import os
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import StreamingResponse
import httpx

from application.service.pricing import PricingGatewayService

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
#  Routes Pricing (via RabbitMQ RPC)
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
