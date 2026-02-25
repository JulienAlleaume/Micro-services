from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import Session

from domain.entities import Price
from infrastructure.db.schema import PriceSchema as PriceDB


class PriceRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, price_id: int) -> Price:
        result = self.session.get(PriceDB, price_id)
        if not result:
            raise Exception(f"Price with id {price_id} not found")
        return self._to_domain(result)

    def get_by_product_id(self, product_id: int) -> Price:
        result = self.session.execute(
            select(PriceDB).where(PriceDB.product_id == product_id)
        ).scalar_one_or_none()
        if not result:
            raise Exception(f"Price for product {product_id} not found")
        return self._to_domain(result)

    def get_all(self) -> List[Price]:
        results = self.session.execute(select(PriceDB)).scalars().all()
        return [self._to_domain(r) for r in results]

    def create(self, price: Price) -> Price:
        db_price = PriceDB(
            product_id=price.product_id,
            product_name=price.product_name,
            amount=price.amount,
            currency=price.currency,
        )
        self.session.add(db_price)
        self.session.commit()
        self.session.refresh(db_price)
        return self._to_domain(db_price)

    def update(self, price_id: int, amount: float, currency: Optional[str] = None) -> Price:
        db_price = self.session.get(PriceDB, price_id)
        if not db_price:
            raise Exception(f"Price with id {price_id} not found")
        db_price.amount = amount
        if currency is not None:
            db_price.currency = currency
        self.session.commit()
        self.session.refresh(db_price)
        return self._to_domain(db_price)

    @staticmethod
    def _to_domain(db: PriceDB) -> Price:
        # Les annotations de type sur PriceSchema garantissent que ces
        # attributs sont correctement typés ; pas besoin de cast().
        return Price(
            id=db.id,
            product_id=db.product_id,
            product_name=db.product_name,
            amount=db.amount,
            currency=db.currency,
        )
