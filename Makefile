ifneq (,$(wildcard ./.env))
	include .env
endif

# dbmate options
DATABASE_URL ?= "mysql://$(RDB_USER):$(RDB_PASS)@$(RDB_HOST):$(RDB_PORT)/$(RDB_NAME)"
DBMATE_MIGRATIONS_DIR ?= "schema/rdb/migrations"
DBMATE_SCHEMA_FILE ?= "schema/rdb/schema.sql"

MIGRATION_COMMENT ?= $(shell bash -c 'read -p "Comments: " pwd; echo $$pwd')

migrate-new:
	dbmate -u $(DATABASE_URL) -d $(DBMATE_MIGRATIONS_DIR) -s $(DBMATE_SCHEMA_FILE) new $(MIGRATION_COMMENT)

migrate-status:
	dbmate -u $(DATABASE_URL) -d $(DBMATE_MIGRATIONS_DIR) -s $(DBMATE_SCHEMA_FILE) status

## migrate-up: proceed db migration
migrate-up:
	dbmate -u $(DATABASE_URL) -d $(DBMATE_MIGRATIONS_DIR) -s $(DBMATE_SCHEMA_FILE) up

## migrate-down: rollback db migration
migrate-down:
	dbmate -u $(DATABASE_URL) -d $(DBMATE_MIGRATIONS_DIR) -s $(DBMATE_SCHEMA_FILE) down

## migrate-drop: drop database
migrate-drop:
	dbmate -u $(DATABASE_URL) -d $(DBMATE_MIGRATIONS_DIR) -s $(DBMATE_SCHEMA_FILE) drop

migrate-reset: migrate-drop migrate-up migrate-seed

gen-db-schema:
	mysqldump --no-data -h$(RDB_HOST) -u$(RDB_USER) -p$(RDB_PASS) $(RDB_NAME)