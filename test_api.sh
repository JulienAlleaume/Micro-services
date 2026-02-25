#!/bin/bash
# ──────────────────────────────────────────────────────────
#  WoW Shop — test_api.sh
#  Teste tous les endpoints exposés par la Gateway (:8000)
# ──────────────────────────────────────────────────────────

BASE_URL="http://localhost:8000"
GREEN="\033[0;32m"; YELLOW="\033[1;33m"; CYAN="\033[0;36m"; RED="\033[0;31m"; RESET="\033[0m"

sep()   { echo -e "${CYAN}────────────────────────────────────${RESET}"; }
title() { echo -e "\n${YELLOW}$1${RESET}"; sep; }
ok()    { echo -e "${GREEN}[OK]${RESET} $1\n"; }

# ── PRODUCTS ─────────────────────────────────────────────

title "1. Création d'une monture (POST /products/)"
curl -s -X POST "$BASE_URL/products/" \
  -H 'Content-Type: application/json' \
  -d '{"name":"Rênes Invincible","description":"Le destrier du Roi Liche.","category":"mount","image_url":"https://wow.zamimg.com/invincible.jpg"}' \
  | python3 -m json.tool && ok "Produit créé"

title "2. Création d'une arme (POST /products/)"
curl -s -X POST "$BASE_URL/products/" \
  -H 'Content-Type: application/json' \
  -d '{"name":"Deuillegivre","description":"Lame du Roi Liche.","category":"weapon","image_url":"https://wow.zamimg.com/frostmourne.jpg"}' \
  | python3 -m json.tool && ok "Produit créé"

title "3. Liste de tous les produits (GET /products/)"
curl -s "$BASE_URL/products/" | python3 -m json.tool && ok "Liste récupérée"

title "4. Produit par ID (GET /products/1)"
curl -s "$BASE_URL/products/1" | python3 -m json.tool && ok "Produit récupéré"

title "5. Catégorie invalide — doit retourner 422 (POST /products/)"
STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$BASE_URL/products/" \
  -H 'Content-Type: application/json' \
  -d '{"name":"Objet","category":"invalid_category"}')
echo "HTTP status: $STATUS"
[ "$STATUS" == "422" ] && ok "Erreur 422 correctement retournée" \
  || echo -e "${RED}[KO]${RESET} Attendu 422, reçu $STATUS"

# ── PRICES ───────────────────────────────────────────────

title "6. Liste de tous les prix (GET /prices/)"
curl -s "$BASE_URL/prices/" | python3 -m json.tool && ok "Prix récupérés"

title "7. Prix du produit ID 1 (GET /prices/product/1)"
curl -s "$BASE_URL/prices/product/1" | python3 -m json.tool && ok "Prix récupéré"

title "8. Mise à jour du prix ID 1 (PUT /prices/1)"
curl -s -X PUT "$BASE_URL/prices/1" \
  -H 'Content-Type: application/json' \
  -d '{"amount": 999, "currency": "gold"}' \
  | python3 -m json.tool && ok "Prix mis à jour"

# ── INVENTORY ────────────────────────────────────────────

title "9. Liste de tout l'inventaire (GET /inventory/)"
curl -s "$BASE_URL/inventory/" | python3 -m json.tool && ok "Inventaire récupéré"

title "10. Inventaire du produit ID 1 (GET /inventory/1)"
curl -s "$BASE_URL/inventory/1" | python3 -m json.tool && ok "Inventaire récupéré"

title "11. Mise à jour du stock — entrepôt 1 / produit 1 (PATCH /inventory/1/1)"
curl -s -X PATCH "$BASE_URL/inventory/1/1" \
  -H 'Content-Type: application/json' \
  -d '{"quantity": 42}' \
  | python3 -m json.tool && ok "Stock mis à jour"

title "12. Vérification du nouveau stock (GET /inventory/1)"
curl -s "$BASE_URL/inventory/1" | python3 -m json.tool

sep
echo -e "\n${GREEN}Tests terminés.${RESET}\n"
