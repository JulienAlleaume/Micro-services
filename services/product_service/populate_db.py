import os
import random
import json
import urllib.request
import urllib.error

# URL de base de l'API (à adapter si besoin)
API_URL = "http://localhost:8000/products/"

# Configuration
STATIC_DIR = "static"
# Mapping : Nom du dossier dans static -> Valeur de la catégorie pour l'API
# ATTENTION : Ces catégories doivent être valides dans votre Enum ProductCategory (domain/models.py)
CATEGORY_MAPPING = {
    "weapons": "weapon",
    "armour": "armor"
}

# Données pour la génération de texte
ADJECTIVES = ["Flamboyant", "Glacial", "Maudit", "Divin", "Ancestral", "Runique", "Sombre", "Céleste"]
WEAPON_TYPES = ["Hache", "Épée", "Dague", "Masse", "Bâton", "Arc"]
ARMOR_TYPES = ["Plastron", "Casque", "Jambières", "Gantelets", "Bottes", "Bouclier"]

def generate_payload(filename, folder):
    """Génère les données d'un produit à partir d'un fichier image."""
    category = CATEGORY_MAPPING.get(folder, "misc")
    
    # Génération du nom et description selon la catégorie
    if category == "weapon":
        name = f"{random.choice(WEAPON_TYPES)} {random.choice(ADJECTIVES)}"
        description = "Une arme forgée dans des matériaux rares, vibrant d'une énergie latente."
    elif category == "armor":
        name = f"{random.choice(ARMOR_TYPES)} {random.choice(ADJECTIVES)}"
        description = "Une protection robuste capable d'encaisser les coups les plus violents."
    else:
        name = f"Objet {random.choice(ADJECTIVES)}"
        description = "Un objet mystérieux."

    # Construction de l'URL de l'image (doit correspondre au montage StaticFiles dans main.py)
    image_url = f"http://localhost:8000/static/{folder}/{filename}"

    return {
        "name": name,
        "description": description,
        "category": category,
        "image_url": image_url
    }

def post_product(data):
    """Envoie une requête POST à l'API pour créer le produit."""
    try:
        json_data = json.dumps(data).encode('utf-8')
        req = urllib.request.Request(
            API_URL,
            data=json_data,
            headers={'Content-Type': 'application/json'}
        )
        
        with urllib.request.urlopen(req) as response:
            if response.status in (200, 201):
                print(f"[OK] {data['name']}")
            else:
                print(f"[STATUS {response.status}] {data['name']}")
                
    except urllib.error.HTTPError as e:
        # Affiche le détail de l'erreur (utile si la catégorie est invalide par exemple)
        error_content = e.read().decode()
        print(f"[ERREUR] {data['name']} : {e.code} - {error_content}")
    except Exception as e:
        print(f"[EXCEPTION] {e}")

def main():
    print(f"--- Démarrage de l'import depuis {STATIC_DIR} ---")
    
    if not os.path.exists(STATIC_DIR):
        print(f"Erreur: Le dossier '{STATIC_DIR}' n'existe pas.")
        return

    for folder, category in CATEGORY_MAPPING.items():
        folder_path = os.path.join(STATIC_DIR, folder)
        
        if not os.path.exists(folder_path):
            print(f"Dossier introuvable : {folder_path} (ignoré)")
            continue
            
        files = [f for f in os.listdir(folder_path) if f.lower().endswith('.png')]
        
        if not files:
            print(f"Aucun PNG trouvé dans {folder}")
            continue
            
        print(f"Traitement de '{folder}' ({len(files)} images)...")
        
        for filename in files:
            payload = generate_payload(filename, folder)
            post_product(payload)

    print("--- Import terminé ---")

if __name__ == "__main__":
    main()