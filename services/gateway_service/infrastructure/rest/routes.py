import os
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
import httpx

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


# --- Routes de la Gateway ---

@router.api_route(
    "/{path:path}",
    methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
)
async def gateway_entrypoint(path: str, request: Request):
    """
    Point d'entrée unique de la Gateway.
    Redirige chaque requête vers le microservice approprié selon le préfixe du path.
    """
    if path.startswith("products") or path.startswith("static"):
        return await _proxy_request(request, PRODUCT_SERVICE_URL)

    return {"message": "Gateway: route non gérée", "path": path}
