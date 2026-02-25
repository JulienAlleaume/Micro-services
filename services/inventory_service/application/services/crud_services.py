from typing import List
from domain.entities import Inventory
from infrastructure.db.repository import InventoryRepository


class InventoryService:
    def __init__(self, repository: InventoryRepository):
        self.repository = repository

    def get_all(self) -> List[Inventory]:
        """Recupere la liste complete de l'inventaire."""
        return self.repository.get_all()

    def get_by_product(self, product_id: int) -> List[Inventory]:
        """Recupere l'inventaire pour un produit donne (tous entrepots)."""
        return self.repository.get_by_product_id(product_id)

    def get_by_warehouse_and_product(self, warehouse_id: int, product_id: int) -> Inventory:
        """Recupere l'inventaire pour un entrepot/produit specifique."""
        return self.repository.get_by_warehouse_and_product(warehouse_id, product_id)

    def create(self, inventory: Inventory) -> Inventory:
        """Cree une nouvelle ligne d'inventaire."""
        return self.repository.create(inventory)

    def update_quantity(self, warehouse_id: int, product_id: int, quantity: int) -> Inventory:
        """Met a jour la quantite en stock."""
        return self.repository.update_quantity(warehouse_id, product_id, quantity)

    def decrement_stock(self, warehouse_id: int, product_id: int, amount: int) -> Inventory:
        """Decremente le stock (appele quand une order line est creee)."""
        return self.repository.decrement_stock(warehouse_id, product_id, amount)
