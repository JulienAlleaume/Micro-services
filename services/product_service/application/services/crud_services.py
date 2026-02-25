from typing import List
from domain.entities import Product
from domain.events import ProductCreatedEvent
from infrastructure.db.repositories import ProductRepository


class ProductService:
    def __init__(self, repository: ProductRepository, event_publisher=None):
        self.repository = repository
        self.event_publisher = event_publisher

    def get_product(self, product_id: int) -> Product:
        """Récupère un produit par son ID."""
        return self.repository.get_product(product_id)

    def get_all_products(self) -> List[Product]:
        """Récupère la liste complète des produits."""
        return self.repository.get_all_products()

    def create_product(self, product: Product) -> Product:
        """Crée un nouveau produit et publie l'événement ProductCreated."""
        created = self.repository.create_product(product)

        # Publie l'événement si un publisher est configuré
        if self.event_publisher:
            event = ProductCreatedEvent(
                product_id=created.id,
                name=created.name,
                category=created.category,
            )
            try:
                self.event_publisher.publish_product_created(event)
            except Exception as e:
                print(f"Failed to publish event: {e}")

        return created
