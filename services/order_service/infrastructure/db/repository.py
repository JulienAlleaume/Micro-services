from typing import List
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from domain.entities import Order, OrderLine, OrderStatus
from infrastructure.db.schema import OrderSchema as OrderDB, OrderLineSchema as OrderLineDB


class OrderRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, order_id: int) -> Order:
        result = self.session.execute(
            select(OrderDB)
            .where(OrderDB.id == order_id)
            .options(selectinload(OrderDB.lines))
        ).scalar_one_or_none()
        if not result:
            raise Exception(f"Order with id {order_id} not found")
        return self._to_domain(result)

    def get_all(self) -> List[Order]:
        results = (
            self.session.execute(
                select(OrderDB).options(selectinload(OrderDB.lines))
            )
            .scalars()
            .all()
        )
        return [self._to_domain(r) for r in results]

    def create(self, order: Order) -> Order:
        db_order = OrderDB(
            customer_id=order.customer_id,
            status=order.status,
            total=order.total,
        )
        for line in order.lines:
            db_line = OrderLineDB(
                product_id=line.product_id,
                product_name=line.product_name,
                quantity=line.quantity,
                unit_price=line.unit_price,
            )
            db_order.lines.append(db_line)
        self.session.add(db_order)
        self.session.commit()
        self.session.refresh(db_order)
        return self._to_domain(db_order)

    def update_status(self, order_id: int, status: str) -> Order:
        db_order = self.session.execute(
            select(OrderDB)
            .where(OrderDB.id == order_id)
            .options(selectinload(OrderDB.lines))
        ).scalar_one_or_none()
        if not db_order:
            raise Exception(f"Order with id {order_id} not found")
        db_order.status = status
        self.session.commit()
        self.session.refresh(db_order)
        return self._to_domain(db_order)

    @staticmethod
    def _to_domain(db: OrderDB) -> Order:
        lines = [
            OrderLine(
                id=l.id,
                order_id=l.order_id,
                product_id=l.product_id,
                product_name=l.product_name,
                quantity=l.quantity,
                unit_price=l.unit_price,
            )
            for l in db.lines
        ]
        return Order(
            id=db.id,
            customer_id=db.customer_id,
            status=OrderStatus(db.status),
            total=db.total,
            lines=lines,
        )
