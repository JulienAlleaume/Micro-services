from typing import List
from domain.models import Product
from infrastructure.db.repositories import ProductRepository

class ProductService:
    def __init__(self, 
        repository: ProductRepository,
    ):
        self.repository = repository

    def get_product(self, product_id: int) -> Product:
        """Récupère un produit par son ID."""
        # Le repository se charge de lever une exception si non trouvé
        return self.repository.get_product(product_id)

    def get_all_products(self) -> List[Product]:
        """Récupère la liste complète des produits."""
        return self.repository.get_all_products()

    def create_product(self, product: Product) -> Product:
        """Crée un nouveau produit après validation métier."""
        # C'est ici qu'on ajouterait de la logique métier supplémentaire si besoin
        # (ex: vérifier si l'utilisateur a le droit de créer, envoyer une notif, etc.)
        return self.repository.create_product(product)
    