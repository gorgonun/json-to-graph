SHELL := /bin/bash

.EXPORT_ALL_VARIABLES:

# basic or full
profile ?= basic

# delete saved configurations and start from scratch
clean ?= false

# mongodb
mongodb_root_username ?= root
mongodb_root_password ?= root
mongodb_database ?= test
mongodb_collection ?= nyt
mongodb_url ?= "mongodb://$(mongodb_root_username):$(mongodb_root_password)@mongodb:27017/$(mongodb_database)?authSource=admin"

# neo4j
neo4j_user ?= neo4j
neo4j_password ?= admin

define GLOBAL_ENV
MONGODB_DATA=./data/mongodb/
NEO4J_DATA=./data/neo4j/
MONGODB_URL="mongodb://$(mongodb_root_username):$(mongodb_root_password)@localhost:27017/$(mongodb_database)?authSource=admin"
MONGODB_COLLECTION=$(mongodb_collection)
MONGODB_DATABASE=$(mongodb_database)
NEO4J_URL="bolt://localhost:7687"
NEO4J_USER=$(neo4j_user)
NEO4J_PASSWORD=$(neo4j_password)
endef

define MONGODB_DEFAULT_ENV
MONGO_INITDB_ROOT_USERNAME=$(mongodb_root_username)
MONGO_INITDB_ROOT_PASSWORD=$(mongodb_root_password)
MONGO_INITDB_DATABASE=$(mongodb_database)
endef

define MONGO_EXPRESS_ENV
ME_CONFIG_MONGODB_URL=$(mongodb_url)
ME_CONFIG_MONGODB_ADMINUSERNAME=root
ME_CONFIG_MONGODB_ADMINPASSWORD=root
endef

define NEO4J_DEFAULT_ENV
NEO4J_AUTH=$(neo4j_user)/$(neo4j_password)
NEO4J_dbms_security_auth__minimum__password__length=1
endef

define MONGO_SEED_DEFAULT_ENV
MONGO_SEED_MONGODB_URL=$(mongodb_url)
MONGO_SEED_MONGODB_COLLECTION=$(mongodb_collection)
endef

write_env_values:
	@echo "$$MONGODB_DEFAULT_ENV" > .env.mongodb
	@echo "$$NEO4J_DEFAULT_ENV" > .env.neo4j
	@echo "$$MONGO_EXPRESS_ENV" > .env.mongo_express
	@echo "$$MONGO_SEED_DEFAULT_ENV" > .env.mongo_seed
	@echo "$$GLOBAL_ENV" > .env

setup_env_file:
	@if [[ "$(clean)" = "true" ]]; \
	then \
	  $(MAKE) write_env_values; \
	else \
	  test -f .env || $(MAKE) write_env_values; \
	fi

start_infra: setup_env_file
	docker-compose --profile $(profile) up -d

stop_infra: setup_env_file
	docker-compose --profile $(profile) down

run: setup_env_file
	cd src/ && poetry run python -m python.main
