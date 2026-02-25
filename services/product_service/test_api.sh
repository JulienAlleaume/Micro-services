#!/bin/bash

BASE_URL="http://localhost:8000"

echo "--- 1. Création d'une monture (Invincible) ---"
curl -X 'POST' \
  "$BASE_URL/products/" \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Rênes d'\''Invincible",
  "description": "Le destrier du Roi Liche.",
  "category": "mount",
  "image_url": "https://wow.zamimg.com/invincible.jpg"
}'
echo -e "\n"

echo "--- 2. Création d'une mascotte (Mini Ragnaros) ---"
curl -X 'POST' \
  "$BASE_URL/products/" \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Mini Ragnaros",
  "description": "Il met le feu partout.",
  "category": "pet",
  "image_url": "https://wow.zamimg.com/ragnaros.jpg"
}'
echo -e "\n"

echo "--- 3. Récupération de tous les produits ---"
curl -X 'GET' "$BASE_URL/products/" | python3 -m json.tool
echo -e "\n"

echo "--- 4. Récupération du produit ID 1 ---"
curl -X 'GET' "$BASE_URL/products/1" | python3 -m json.tool
echo -e "\n"

echo "--- 5. Test d'erreur (Catégorie invalide) ---"
# On essaie de créer une "weapon" qui n'existe pas dans l'Enum
curl -X 'POST' \
  "$BASE_URL/products/" \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Deuillegivre",
  "category": "weapon"
}'
echo -e "\n"
