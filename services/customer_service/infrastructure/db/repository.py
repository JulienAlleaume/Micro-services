from typing import List
from sqlalchemy import select
from sqlalchemy.orm import Session

from domain.entities import Customer
from infrastructure.db.schema import CustomerSchema as CustomerDB


class CustomerRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, customer_id: int) -> Customer:
        result = self.session.get(CustomerDB, customer_id)
        if not result:
            raise Exception(f"Customer with id {customer_id} not found")
        return self._to_domain(result)

    def get_all(self) -> List[Customer]:
        results = self.session.execute(select(CustomerDB)).scalars().all()
        return [self._to_domain(r) for r in results]

    def create(self, customer: Customer) -> Customer:
        db_customer = CustomerDB(
            username=customer.username,
            email=customer.email,
            gold_balance=customer.gold_balance,
            is_active=customer.is_active,
        )
        self.session.add(db_customer)
        self.session.commit()
        self.session.refresh(db_customer)
        return self._to_domain(db_customer)

    def update(self, customer_id: int, data: dict) -> Customer:
        db_customer = self.session.get(CustomerDB, customer_id)
        if not db_customer:
            raise Exception(f"Customer with id {customer_id} not found")
        for key, value in data.items():
            if hasattr(db_customer, key):
                setattr(db_customer, key, value)
        self.session.commit()
        self.session.refresh(db_customer)
        return self._to_domain(db_customer)

    @staticmethod
    def _to_domain(db: CustomerDB) -> Customer:
        return Customer(
            id=db.id,
            username=db.username,
            email=db.email,
            gold_balance=db.gold_balance,
            is_active=db.is_active,
        )
