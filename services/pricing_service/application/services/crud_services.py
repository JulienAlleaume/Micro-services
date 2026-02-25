from typing import List, Optional
from domain.entities import Price
from infrastructure.db.repository import PriceRepository


class PricingService:
    def __init__(self, repository: PriceRepository):
        self.repository = repository

    def get_price(self, price_id: int) -> Price:
        """Récupère un prix par son ID."""
        return self.repository.get_by_id(price_id)

    def get_price_by_product(self, product_id: int) -> Price:
        """Récupère le prix associé à un produit."""
        return self.repository.get_by_product_id(product_id)

    def get_all_prices(self) -> List[Price]:
        """Récupère la liste complète des prix."""
        return self.repository.get_all()

    def create_price(self, price: Price) -> Price:
        """Crée un nouveau prix."""
        return self.repository.create(price)

    def update_price(self, price_id: int, amount: float, currency: Optional[str] = None) -> Price:
        """Met à jour un prix existant."""
        return self.repository.update(price_id, amount, currency)
