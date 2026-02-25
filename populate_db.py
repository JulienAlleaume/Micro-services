import os
import random
import json
import urllib.request
import urllib.error

# ── Configuration ─────────────────────────────────────────────────
GATEWAY_URL       = os.getenv("GATEWAY_URL", "http://localhost:8000")
PRODUCTS_ENDPOINT = f"{GATEWAY_URL}/products/"

# Dossier static relatif à la racine du projet
STATIC_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "services", "product_service", "infrastructure", "static",
)

# Mapping : nom du dossier local -> catégorie API
CATEGORY_MAPPING = {
    "weapons": "weapon",
    "armour":  "armor",
}

# ── Données de génération ─────────────────────────────────────────
ADJECTIVES   = ["Flamboyant", "Glacial", "Maudit", "Divin", "Ancestral", "Runique", "Sombre", "Céleste"]
WEAPON_TYPES = ["Hache", "Épée", "Dague", "Masse", "Bâton", "Arc"]
ARMOR_TYPES  = ["Plastron", "Casque", "Jambières", "Gantelets", "Bottes", "Bouclier"]


def generate_payload(filename: str, folder: str) -> dict:
    """Génère les données d'un produit à partir d'un fichier image."""
    category = CATEGORY_MAPPING.get(folder, "misc")

    if category == "weapon":
        name        = f"{random.choice(WEAPON_TYPES)} {random.choice(ADJECTIVES)}"
        description = "Une arme forgée dans des matériaux rares, vibrant d'une énergie latente."
    elif category == "armor":
        name        = f"{random.choice(ARMOR_TYPES)} {random.choice(ADJECTIVES)}"
        description = "Une protection robuste capable d'encaisser les coups les plus violents."
    else:
        name        = f"Objet {random.choice(ADJECTIVES)}"
        description = "Un objet mystérieux."

    # L'URL image passe par la gateway qui la proxifie vers product_service
    image_url = f"{GATEWAY_URL}/static/{folder}/{filename}"

    return {
        "name":        name,
        "description": description,
        "category":    category,
        "image_url":   image_url,
    }


def post_product(data: dict) -> bool:
    """Envoie une requête POST à la gateway pour créer le produit."""
    try:
        json_data = json.dumps(data).encode("utf-8")
        req = urllib.request.Request(
            PRODUCTS_ENDPOINT,
            data=json_data,
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read())
            print(f"  [OK] {data['name']} → id={result.get('id')}")
            return True
    except urllib.error.HTTPError as e:
        print(f"  [HTTP {e.code}] {data['name']} — {e.read().decode()}")
    except Exception as e:
        print(f"  [ERREUR] {e}")
    return False


def main():
    print(f"Gateway : {GATEWAY_URL}")
    print(f"Static  : {STATIC_DIR}\n")

    if not os.path.exists(STATIC_DIR):
        print(f"Erreur : le dossier '{STATIC_DIR}' est introuvable.")
        return

    total_ok = 0
    total_ko = 0

    for folder, category in CATEGORY_MAPPING.items():
        folder_path = os.path.join(STATIC_DIR, folder)

        if not os.path.exists(folder_path):
            print(f"Dossier introuvable : {folder_path} (ignoré)")
            continue

        files = sorted(f for f in os.listdir(folder_path) if f.lower().endswith(".png"))

        if not files:
            print(f"Aucun PNG dans {folder} (ignoré)")
            continue

        print(f"--- {folder} ({len(files)} images, catégorie '{category}') ---")
        for filename in files:
            payload = generate_payload(filename, folder)
            if post_product(payload):
                total_ok += 1
            else:
                total_ko += 1

    print(f"\nImport terminé : {total_ok} OK / {total_ko} erreur(s)")


if __name__ == "__main__":
    main()