import os
from fastapi import APIRouter, HTTPException
import httpx

from application.service.pricing import PricingGatewayService
from application.service.inventory import InventoryGatewayService
from application.service.customer import CustomerGatewayService
from application.service.order import OrderGatewayService

PRODUCT_SERVICE_URL = os.getenv("PRODUCT_SERVICE_URL", "http://product_service:8001")

# ──────────────────────────────────────────────
#  Product  (proxy HTTP vers product_service)
# ──────────────────────────────────────────────
product_router = APIRouter(prefix="/products", tags=["Products"])


@product_router.get("/")
async def get_all_products():
    """Liste tous les produits."""
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{PRODUCT_SERVICE_URL}/products/")
        return r.json()


@product_router.get("/{product_id}")
async def get_product(product_id: int):
    """Recupere un produit par son ID."""
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{PRODUCT_SERVICE_URL}/products/{product_id}")
        if r.status_code == 404:
            raise HTTPException(status_code=404, detail="Produit non trouve")
        return r.json()


@product_router.post("/", status_code=201)
async def create_product(request_body: dict):
    """Cree un nouveau produit."""
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{PRODUCT_SERVICE_URL}/products/", json=request_body)
        if r.status_code >= 400:
            raise HTTPException(status_code=r.status_code, detail=r.json().get("detail", r.text))
        return r.json()


# ──────────────────────────────────────────────
#  Pricing  (ZMQ RPC)
# ──────────────────────────────────────────────
pricing_router = APIRouter(prefix="/prices", tags=["Pricing"])


@pricing_router.get("/")
def get_all_prices():
    """Liste tous les prix."""
    try:
        return PricingGatewayService().get_all_prices()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@pricing_router.get("/product/{product_id}")
def get_price_by_product(product_id: int):
    """Recupere le prix associe a un produit."""
    try:
        return PricingGatewayService().get_price_by_product(product_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@pricing_router.get("/{price_id}")
def get_price(price_id: int):
    """Recupere un prix par son ID."""
    try:
        return PricingGatewayService().get_price(price_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@pricing_router.post("/", status_code=201)
def create_price(request_body: dict):
    """Cree un nouveau prix."""
    try:
        return PricingGatewayService().create_price(request_body)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@pricing_router.put("/{price_id}")
def update_price(price_id: int, request_body: dict):
    """Met a jour un prix existant."""
    try:
        return PricingGatewayService().update_price(price_id, request_body)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ──────────────────────────────────────────────
#  Inventory  (ZMQ RPC)
# ──────────────────────────────────────────────
inventory_router = APIRouter(prefix="/inventory", tags=["Inventory"])


@inventory_router.get("/")
def get_all_inventory():
    """Liste tout l'inventaire."""
    try:
        return InventoryGatewayService().get_all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@inventory_router.get("/{product_id}")
def get_inventory_by_product(product_id: int):
    """Recupere l'inventaire pour un produit donne."""
    try:
        return InventoryGatewayService().get_by_product(product_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@inventory_router.patch("/{warehouse_id}/{product_id}")
def update_inventory(warehouse_id: int, product_id: int, request_body: dict):
    """Met a jour la quantite en stock pour un entrepot/produit."""
    try:
        return InventoryGatewayService().update_quantity(warehouse_id, product_id, request_body)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ──────────────────────────────────────────────
#  Warehouses  (ZMQ RPC via inventory_service)
# ──────────────────────────────────────────────
warehouse_router = APIRouter(prefix="/warehouses", tags=["Warehouses"])


@warehouse_router.get("/")
def get_all_warehouses():
    """Liste tous les entrepots."""
    try:
        return InventoryGatewayService().get_all_warehouses()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@warehouse_router.get("/{warehouse_id}")
def get_warehouse(warehouse_id: int):
    """Recupere un entrepot par son ID."""
    try:
        return InventoryGatewayService().get_warehouse(warehouse_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@warehouse_router.post("/", status_code=201)
def create_warehouse(request_body: dict):
    """Cree un nouvel entrepot."""
    try:
        return InventoryGatewayService().create_warehouse(request_body)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ──────────────────────────────────────────────
#  Customer  (ZMQ RPC)
# ──────────────────────────────────────────────
customer_router = APIRouter(prefix="/customers", tags=["Customers"])


@customer_router.get("/")
def get_all_customers():
    """Liste tous les clients."""
    try:
        return CustomerGatewayService().get_all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@customer_router.get("/{customer_id}")
def get_customer(customer_id: int):
    """Recupere un client par son ID."""
    try:
        return CustomerGatewayService().get_by_id(customer_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@customer_router.post("/", status_code=201)
def create_customer(request_body: dict):
    """Cree un nouveau client."""
    try:
        return CustomerGatewayService().create(request_body)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@customer_router.put("/{customer_id}")
def update_customer(customer_id: int, request_body: dict):
    """Met a jour un client existant."""
    try:
        return CustomerGatewayService().update(customer_id, request_body)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ──────────────────────────────────────────────
#  Order  (ZMQ RPC)
# ──────────────────────────────────────────────
order_router = APIRouter(prefix="/orders", tags=["Orders"])


@order_router.get("/")
def get_all_orders():
    """Liste toutes les commandes."""
    try:
        return OrderGatewayService().get_all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@order_router.get("/{order_id}")
def get_order(order_id: int):
    """Recupere une commande par son ID."""
    try:
        return OrderGatewayService().get_by_id(order_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@order_router.post("/", status_code=201)
def create_order(request_body: dict):
    """Cree une nouvelle commande."""
    try:
        return OrderGatewayService().create(request_body)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@order_router.patch("/{order_id}")
def update_order_status(order_id: int, request_body: dict):
    """Met a jour le statut d'une commande."""
    try:
        return OrderGatewayService().update_status(order_id, request_body)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
