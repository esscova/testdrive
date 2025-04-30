# Makefile para gerenciar o ambiente MongoDB

# variaveis
COMPOSE_FILE = docker-compose.yml
MONGO_CONTAINER = mongodb
MONGO_URI = mongodb://admin:admin123@localhost:27017/testdb?authSource=admin

# Iniciar o ambiente MongoDB
up:
	docker compose -f $(COMPOSE_FILE) up -d

# Parar o ambiente MongoDB
down:
	docker compose -f $(COMPOSE_FILE) down

# Parar o ambiente e remover volumes
down-v:
	docker compose -f $(COMPOSE_FILE) down -v

# Acessar o shell do MongoDB
mongo-shell:
	@if ! docker ps -q -f name=$(MONGO_CONTAINER) | grep -q .; then \
		echo "Erro: O container $(MONGO_CONTAINER) não está rodando. Execute 'make up' primeiro."; \
		exit 1; \
	fi
	docker exec -it $(MONGO_CONTAINER) mongosh "$(MONGO_URI)"

# Importar um arquivo JSON específico ... exemplo: make import-json FILE=exemplo.json
import-json:
	@if [ -z "$(FILE)" ]; then \
		echo "Erro: Defina o arquivo JSON com FILE=<nome>. Ex: make import-json FILE=exemplo.json"; \
		exit 1; \
	fi
	@if ! docker ps -q -f name=$(MONGO_CONTAINER) | grep -q .; then \
		echo "Erro: O container $(MONGO_CONTAINER) não está rodando. Execute 'make up' primeiro."; \
		exit 1; \
	fi
	docker exec $(MONGO_CONTAINER) mongoimport --uri "$(MONGO_URI)" --collection $(basename $(FILE) .json) --file /dados/$(FILE) --jsonArray

# logs do container MongoDB
logs:
	docker logs $(MONGO_CONTAINER)

# Exibir ajuda
help:
	@echo "Comandos disponíveis:"
	@echo "  make up           - Inicia o ambiente MongoDB"
	@echo "  make down         - Para o ambiente MongoDB"
	@echo "  make down-v       - Para o ambiente e remove volumes"
	@echo "  make mongo-shell  - Acessa o shell do MongoDB (mongosh)"
	@echo "  make import-json FILE=<nome>.json - Importa um arquivo JSON para o banco testdb"
	@echo "  make logs         - Exibe logs do container MongoDB"
	@echo "  make help         - Exibe esta ajuda"
