from typing import List
from sqlalchemy import select
from sqlalchemy.orm import Session

from domain.entities import Product, ProductCategory
from infrastructure.db.schema import ProductShema as ProductDB


class ProductRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_product(self, product_id: int) -> Product:
        result = self.session.execute(
            select(ProductDB).where(ProductDB.id == product_id)
        ).scalar_one_or_none()
        if not result:
            raise Exception(f"Product with id {product_id} not found")
        return self._to_domain(result)

    def get_all_products(self) -> List[Product]:
        results = self.session.execute(select(ProductDB)).scalars().all()
        return [self._to_domain(p) for p in results]

    def create_product(self, product: Product) -> Product:
        product_db = ProductDB(
            name=product.name,
            description=product.description,
            category=product.category,
            image_url=product.image_url,
        )
        self.session.add(product_db)
        self.session.commit()
        self.session.refresh(product_db)
        return self._to_domain(product_db)

    @staticmethod
    def _to_domain(db: ProductDB) -> Product:
        return Product(
            id=db.id,
            name=db.name,
            description=db.description,
            category=ProductCategory(db.category),
            image_url=db.image_url,
        )
