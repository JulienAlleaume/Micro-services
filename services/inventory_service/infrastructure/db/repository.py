from typing import List, Optional
from sqlalchemy import select, and_
from sqlalchemy.orm import Session

from domain.entities import Inventory, Warehouse
from infrastructure.db.schema import InventorySchema as InventoryDB, WarehouseSchema as WarehouseDB


class WarehouseRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> List[Warehouse]:
        results = self.session.execute(select(WarehouseDB)).scalars().all()
        return [self._to_domain(r) for r in results]

    def get_by_id(self, warehouse_id: int) -> Warehouse:
        result = self.session.get(WarehouseDB, warehouse_id)
        if not result:
            raise Exception(f"Warehouse with id {warehouse_id} not found")
        return self._to_domain(result)

    def create(self, warehouse: Warehouse) -> Warehouse:
        db_row = WarehouseDB(name=warehouse.name, location=warehouse.location)
        self.session.add(db_row)
        self.session.commit()
        self.session.refresh(db_row)
        return self._to_domain(db_row)

    @staticmethod
    def _to_domain(db: WarehouseDB) -> Warehouse:
        return Warehouse(id=db.id, name=db.name, location=db.location)


class InventoryRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, inventory_id: int) -> Inventory:
        result = self.session.get(InventoryDB, inventory_id)
        if not result:
            raise Exception(f"Inventory with id {inventory_id} not found")
        return self._to_domain(result)

    def get_by_product_id(self, product_id: int) -> List[Inventory]:
        """Retourne toutes les lignes d'inventaire pour un produit (tous entrepots)."""
        results = self.session.execute(
            select(InventoryDB).where(InventoryDB.product_id == product_id)
        ).scalars().all()
        return [self._to_domain(r) for r in results]

    def get_by_warehouse_and_product(self, warehouse_id: int, product_id: int) -> Inventory:
        result = self.session.execute(
            select(InventoryDB).where(
                and_(
                    InventoryDB.warehouse_id == warehouse_id,
                    InventoryDB.product_id == product_id,
                )
            )
        ).scalar_one_or_none()
        if not result:
            raise Exception(
                f"Inventory for warehouse {warehouse_id} / product {product_id} not found"
            )
        return self._to_domain(result)

    def get_all(self) -> List[Inventory]:
        results = self.session.execute(select(InventoryDB)).scalars().all()
        return [self._to_domain(r) for r in results]

    def create(self, inventory: Inventory) -> Inventory:
        db_row = InventoryDB(
            product_id=inventory.product_id,
            product_name=inventory.product_name,
            warehouse_id=inventory.warehouse_id,
            quantity=inventory.quantity,
        )
        self.session.add(db_row)
        self.session.commit()
        self.session.refresh(db_row)
        return self._to_domain(db_row)

    def update_quantity(
        self, warehouse_id: int, product_id: int, quantity: int
    ) -> Inventory:
        result = self.session.execute(
            select(InventoryDB).where(
                and_(
                    InventoryDB.warehouse_id == warehouse_id,
                    InventoryDB.product_id == product_id,
                )
            )
        ).scalar_one_or_none()
        if not result:
            raise Exception(
                f"Inventory for warehouse {warehouse_id} / product {product_id} not found"
            )
        result.quantity = quantity
        self.session.commit()
        self.session.refresh(result)
        return self._to_domain(result)

    def decrement_stock(
        self, warehouse_id: int, product_id: int, amount: int
    ) -> Inventory:
        """Decremente le stock. Leve une exception si stock insuffisant."""
        result = self.session.execute(
            select(InventoryDB).where(
                and_(
                    InventoryDB.warehouse_id == warehouse_id,
                    InventoryDB.product_id == product_id,
                )
            )
        ).scalar_one_or_none()
        if not result:
            raise Exception(
                f"Inventory for warehouse {warehouse_id} / product {product_id} not found"
            )
        if result.quantity < amount:
            raise Exception(
                f"Insufficient stock: {result.quantity} available, {amount} requested"
            )
        result.quantity -= amount
        self.session.commit()
        self.session.refresh(result)
        return self._to_domain(result)

    @staticmethod
    def _to_domain(db: InventoryDB) -> Inventory:
        return Inventory(
            id=db.id,
            product_id=db.product_id,
            product_name=db.product_name,
            warehouse_id=db.warehouse_id,
            quantity=db.quantity,
        )
