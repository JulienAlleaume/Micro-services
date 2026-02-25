#!/usr/bin/env python3
"""
WoW Shop -- populate_db.py
Peuple la base de donnees via la Gateway si elle est vide.
Utilisation : python3 populate_db.py
"""
import os
import random
import json
import urllib.request
import urllib.error
import time

# ── Configuration ─────────────────────────────────────────────────
GATEWAY_URL = os.getenv("GATEWAY_URL", "http://localhost:8000")
DB_MARKER   = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".db_populated")

STATIC_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "services", "product_service", "infrastructure", "static",
)

CATEGORY_MAPPING = {
    "weapons": "weapon",
    "armour":  "armor",
}

# ── Donnees WoW ──────────────────────────────────────────────────
ADJECTIVES   = ["Flamboyant", "Glacial", "Maudit", "Divin", "Ancestral", "Runique", "Sombre", "Celeste"]
WEAPON_TYPES = ["Hache", "Epee", "Dague", "Masse", "Baton", "Arc"]
ARMOR_TYPES  = ["Plastron", "Casque", "Jambieres", "Gantelets", "Bottes", "Bouclier"]

WAREHOUSES = [
    {"name": "Banque de Hurlevent",   "location": "Hurlevent"},
    {"name": "Banque d'Orgrimmar",    "location": "Orgrimmar"},
    {"name": "Caveau de Dalaran",     "location": "Dalaran"},
    {"name": "Coffre des Sacrenuit",  "location": "Suramar"},
    {"name": "Depot de Forgefer",     "location": "Forgefer"},
]

CUSTOMERS = [
    {"username": "arthas",   "email": "arthas@northrend.wow",   "gold_balance": 50000},
    {"username": "thrall",   "email": "thrall@orgrimmar.wow",   "gold_balance": 35000},
    {"username": "jaina",    "email": "jaina@theramore.wow",    "gold_balance": 42000},
    {"username": "sylvanas", "email": "sylvanas@undercity.wow", "gold_balance": 28000},
    {"username": "illidan",  "email": "illidan@blacktemple.wow","gold_balance": 60000},
]


# ── Helpers HTTP ──────────────────────────────────────────────────

def _get(path: str) -> list | dict | None:
    """GET sur la gateway, retourne le JSON ou None."""
    try:
        req = urllib.request.Request(f"{GATEWAY_URL}{path}")
        with urllib.request.urlopen(req, timeout=5) as resp:
            return json.loads(resp.read().decode())
    except Exception:
        return None


def _post(path: str, data: dict) -> dict | None:
    """POST sur la gateway, retourne le JSON ou None."""
    try:
        body = json.dumps(data).encode("utf-8")
        req = urllib.request.Request(
            f"{GATEWAY_URL}{path}",
            data=body,
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print(f"  [HTTP {e.code}] {e.read().decode()[:120]}")
    except Exception as e:
        print(f"  [ERREUR] {e}")
    return None


def _wait_for_gateway(max_retries: int = 20, delay: float = 2.0):
    """Attend que la gateway soit prete."""
    for i in range(max_retries):
        try:
            urllib.request.urlopen(f"{GATEWAY_URL}/products/", timeout=3)
            return True
        except Exception:
            print(f"  En attente de la gateway ({i+1}/{max_retries})...")
            time.sleep(delay)
    return False


# ── Population ────────────────────────────────────────────────────

def populate_warehouses() -> int:
    """Cree les entrepots WoW."""
    print("\n-- Entrepots --")
    count = 0
    for wh in WAREHOUSES:
        result = _post("/warehouses/", wh)
        if result:
            print(f"  [OK] {wh['name']} (id={result.get('id')})")
            count += 1
    return count


def populate_customers() -> int:
    """Cree les clients WoW."""
    print("\n-- Clients --")
    count = 0
    for c in CUSTOMERS:
        result = _post("/customers/", c)
        if result:
            print(f"  [OK] {c['username']} (id={result.get('id')})")
            count += 1
    return count


def populate_products() -> int:
    """Cree les produits a partir des images statiques."""
    print("\n-- Produits --")
    if not os.path.exists(STATIC_DIR):
        print(f"  Dossier '{STATIC_DIR}' introuvable, produits ignores.")
        return 0

    count = 0
    for folder, category in CATEGORY_MAPPING.items():
        folder_path = os.path.join(STATIC_DIR, folder)
        if not os.path.exists(folder_path):
            print(f"  Dossier introuvable : {folder_path} (ignore)")
            continue

        files = sorted(f for f in os.listdir(folder_path) if f.lower().endswith(".png"))
        if not files:
            continue

        print(f"  --- {folder} ({len(files)} images, categorie '{category}') ---")
        for filename in files:
            if category == "weapon":
                name = f"{random.choice(WEAPON_TYPES)} {random.choice(ADJECTIVES)}"
                desc = "Une arme forgee dans des materiaux rares, vibrant d'une energie latente."
            elif category == "armor":
                name = f"{random.choice(ARMOR_TYPES)} {random.choice(ADJECTIVES)}"
                desc = "Une protection robuste capable d'encaisser les coups les plus violents."
            else:
                name = f"Objet {random.choice(ADJECTIVES)}"
                desc = "Un objet mysterieux."

            payload = {
                "name": name,
                "description": desc,
                "category": category,
                "image_url": f"{GATEWAY_URL}/static/{folder}/{filename}",
            }
            result = _post("/products/", payload)
            if result:
                print(f"    [OK] {name} (id={result.get('id')})")
                count += 1
    return count


def populate_inventory(nb_products: int, nb_warehouses: int) -> int:
    """Ajoute du stock aleatoire pour chaque produit dans chaque entrepot."""
    print("\n-- Inventaire (stock aleatoire) --")
    count = 0
    for wh_id in range(1, nb_warehouses + 1):
        for prod_id in range(1, nb_products + 1):
            qty = random.randint(0, 50)
            result = _post("/inventory/", {
                "product_id": prod_id,
                "product_name": f"product_{prod_id}",
                "warehouse_id": wh_id,
                "quantity": qty,
            })
            if result:
                count += 1
    print(f"  [OK] {count} lignes d'inventaire creees")
    return count


# ── Main ──────────────────────────────────────────────────────────

def main():
    print(f"Gateway : {GATEWAY_URL}")
    print(f"Marqueur: {DB_MARKER}")

    # Verification du marqueur .db_populated
    if os.path.exists(DB_MARKER):
        print("\nLe fichier .db_populated existe deja.")
        print("La base est deja peuplee. Supprimez .db_populated pour forcer un re-peuplement.")
        return

    # Attendre que la gateway soit disponible
    print("\nVerification de la gateway...")
    if not _wait_for_gateway():
        print("La gateway n'est pas accessible. Lancez 'docker compose up' d'abord.")
        return

    # Verification supplementaire : si des produits existent deja, on skip
    existing = _get("/products/")
    if existing and len(existing) > 0:
        print(f"\n{len(existing)} produit(s) deja en base. Creation du marqueur et arret.")
        open(DB_MARKER, "w").write("populated\n")
        return

    # Peuplement
    nb_wh   = populate_warehouses()
    nb_cust = populate_customers()
    nb_prod = populate_products()

    # Petit delai pour laisser les SUB ZMQ creer les prix/inventaire par defaut
    if nb_prod > 0:
        print("\n  Attente de 3s pour la propagation ZMQ (prix + inventaire par defaut)...")
        time.sleep(3)

    print(f"\n== Resume ==")
    print(f"  Entrepots : {nb_wh}")
    print(f"  Clients   : {nb_cust}")
    print(f"  Produits  : {nb_prod}")

    # Creation du marqueur
    with open(DB_MARKER, "w") as f:
        f.write("populated\n")
    print(f"\nMarqueur cree : {DB_MARKER}")
    print("Peuplement termine.")


if __name__ == "__main__":
    main()