from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from infrastructure.db.database import SessionLocal
from infrastructure.db.repositories import ProductRepository
from application.services.crud_services import ProductService
from application.dtos import ProductCreateRequest, ProductResponse
from services.product_service.domain.entities import Product, ProductCategory

router = APIRouter()

# --- Injection de Dépendances ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_product_service(db: Session = Depends(get_db)) -> ProductService:
    repository = ProductRepository(db)
    return ProductService(repository)

# --- Routes ---

@router.post("/products/", response_model=ProductResponse, status_code=201)
def create_product(
    product_request: ProductCreateRequest, 
    service: ProductService = Depends(get_product_service)
):
    """Crée un nouvel objet dans la boutique."""
    try:
        # Conversion du DTO (Request) vers le Modèle de Domaine
        category_enum = ProductCategory(product_request.category)
        
        new_product_domain = Product(
            id=0, 
            name=product_request.name,
            description=product_request.description,
            category=category_enum,
            image_url=product_request.image_url
        )
        
        return service.create_product(new_product_domain)

    except ValueError:
        valid_categories = [c.value for c in ProductCategory]
        raise HTTPException(status_code=400, detail=f"Catégorie invalide. Choix possibles : {valid_categories}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/products/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int, 
    service: ProductService = Depends(get_product_service)
):
    """Récupère un objet par son ID."""
    try:
        return service.get_product(product_id)
    except Exception:
        raise HTTPException(status_code=404, detail="Produit non trouvé")

@router.get("/products/", response_model=List[ProductResponse])
def get_all_products(
    service: ProductService = Depends(get_product_service)
):
    """Liste tous les objets en vente."""
    return service.get_all_products()
