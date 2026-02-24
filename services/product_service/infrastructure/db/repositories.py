from typing import List, Optional, cast
from sqlalchemy import select, Select, insert, update, delete
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

# Import du modèle de domaine (Pydantic)
from domain.models import Product, ProductCategory
# Import du modèle de base de données (SQLAlchemy) avec un alias pour éviter les conflits
from infrastructure.db.models import ProductShema as ProductDB

class ProductRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_product(self, product_id: int) -> Product:
        query: Select = select(ProductDB).where(
            ProductDB.id == product_id
        )
        try:
            with self.session as _db:
                result: ProductDB | None = _db.scalar(query)
                if not result:
                    raise Exception("Product not found")
                return Product(
                    id=cast(int, result.id),
                    name=cast(str, result.name),
                    description=cast(Optional[str], result.description),
                    category=cast(ProductCategory, result.category),
                    image_url=cast(Optional[str], result.image_url)
                )
        except SQLAlchemyError as exc:
            raise Exception(f"Error fetching product {product_id}") from exc

    def get_all_products(self) -> List[Product]:
        query: Select = select(ProductDB)
        try:
            with self.session as _db:
                products_db = _db.scalars(query).all()
                
                return [
                    Product(
                        id=cast(int, p.id),
                        name=cast(str, p.name),
                        description=cast(Optional[str], p.description),
                        category=cast(ProductCategory, p.category),
                        image_url=cast(Optional[str], p.image_url)
                    ) for p in products_db
                ]
        except SQLAlchemyError as exc:
            raise Exception("Error fetching all products from DB") from exc

    def create_product(self, product: Product) -> Product:
        try:
            with self.session as _db:
                # Création de l'entité DB à partir du modèle Pydantic
                product_db = ProductDB(
                    name=product.name,
                    description=product.description,
                    category=product.category,
                    image_url=product.image_url
                )
                
                _db.add(product_db)
                _db.commit()
                _db.refresh(product_db) # Récupère l'ID généré par la BDD
                
                return Product(
                    id=cast(int, product_db.id),
                    name=cast(str, product_db.name),
                    description=cast(Optional[str], product_db.description),
                    category=cast(ProductCategory, product_db.category),
                    image_url=cast(Optional[str], product_db.image_url)
                )
        except SQLAlchemyError as exc:
            self.session.rollback()
            raise Exception("Error creating product in DB") from exc
