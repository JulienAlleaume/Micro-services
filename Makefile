.PHONY: help up down build rebuild logs ps \
        logs-product logs-pricing logs-inventory logs-gateway logs-db \
        shell-product shell-pricing shell-inventory shell-gateway shell-db \
        clean prune restart populate test

# ──────────────────────────────────────────────────────────────────
#  Couleurs
# ──────────────────────────────────────────────────────────────────
RESET  := \033[0m
BOLD   := \033[1m
CYAN   := \033[36m
GREEN  := \033[32m
YELLOW := \033[33m
RED    := \033[31m

# ──────────────────────────────────────────────────────────────────
#  Aide
# ──────────────────────────────────────────────────────────────────
help: ## Affiche cette aide
	@echo ""
	@echo "$(BOLD)$(CYAN)WoW Shop — Commandes disponibles$(RESET)"
	@echo "──────────────────────────────────"
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z_-]+:.*##/ { printf "  $(GREEN)%-22s$(RESET) %s\n", $$1, $$2 }' $(MAKEFILE_LIST)
	@echo ""

# ──────────────────────────────────────────────────────────────────
#  Stack
# ──────────────────────────────────────────────────────────────────
up: ## Demarre tous les services (detache)
	docker compose up -d

down: ## Arrete et supprime les conteneurs
	docker compose down

build: ## Construit les images (avec cache)
	docker compose build

rebuild: ## Reconstruit toutes les images sans cache
	docker compose build --no-cache

restart: ## Redémarre tous les services
	docker compose restart

ps: ## Affiche l'état des conteneurs
	docker compose ps

# ──────────────────────────────────────────────────────────────────
#  Logs
# ──────────────────────────────────────────────────────────────────
logs: ## Suit les logs de tous les services
	docker compose logs -f

logs-product: ## Logs du product_service
	docker compose logs -f product_service

logs-pricing: ## Logs du pricing_service
	docker compose logs -f pricing_service

logs-inventory: ## Logs du inventory_service
	docker compose logs -f inventory_service

logs-gateway: ## Logs du gateway_service
	docker compose logs -f gateway_service

logs-db: ## Logs de postgres
	docker compose logs -f postgres

# ──────────────────────────────────────────────────────────────────
#  Shells
# ──────────────────────────────────────────────────────────────────
shell-product: ## Shell dans product_service
	docker compose exec product_service bash

shell-pricing: ## Shell dans pricing_service
	docker compose exec pricing_service bash

shell-inventory: ## Shell dans inventory_service
	docker compose exec inventory_service bash

shell-gateway: ## Shell dans gateway_service
	docker compose exec gateway_service bash

shell-db: ## Shell psql dans postgres
	docker compose exec postgres psql -U $${POSTGRES_USER:-postgres} -d $${POSTGRES_DB:-app_db}

# ──────────────────────────────────────────────────────────────────
#  Nettoyage
# ──────────────────────────────────────────────────────────────────
clean: ## Arrete les conteneurs et supprime les volumes
	docker compose down -v

prune: ## Supprime toutes les images et volumes non utilises (attention)
	docker system prune -f
	docker volume prune -f

# ──────────────────────────────────────────────────────────────────
#  Dev helpers
# ──────────────────────────────────────────────────────────────────
populate: ## Popule la BDD avec les images static (lance populate_db.py)
	python3 populate_db.py

test: ## Lance les tests API (lance test_api.sh)
	bash test_api.sh
