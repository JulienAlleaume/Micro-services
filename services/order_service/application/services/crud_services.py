from typing import List
from domain.entities import Order, OrderLine
from infrastructure.db.repository import OrderRepository


class OrderService:
    def __init__(self, repository: OrderRepository):
        self.repository = repository

    def get_all(self) -> List[Order]:
        return self.repository.get_all()

    def get_by_id(self, order_id: int) -> Order:
        return self.repository.get_by_id(order_id)

    def create(self, order: Order) -> Order:
        # Calcul simple du total : somme(quantity * unit_price)
        order.total = sum(line.quantity * line.unit_price for line in order.lines)
        return self.repository.create(order)

    def update_status(self, order_id: int, status: str) -> Order:
        return self.repository.update_status(order_id, status)
