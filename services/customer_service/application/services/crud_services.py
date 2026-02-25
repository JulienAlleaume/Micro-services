from typing import List
from domain.entities import Customer
from infrastructure.db.repository import CustomerRepository


class CustomerService:
    def __init__(self, repository: CustomerRepository):
        self.repository = repository

    def get_all(self) -> List[Customer]:
        return self.repository.get_all()

    def get_by_id(self, customer_id: int) -> Customer:
        return self.repository.get_by_id(customer_id)

    def create(self, customer: Customer) -> Customer:
        return self.repository.create(customer)

    def update(self, customer_id: int, data: dict) -> Customer:
        return self.repository.update(customer_id, data)
