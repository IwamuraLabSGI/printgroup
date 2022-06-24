ifneq (,$(wildcard ./.env))
	include .env
endif

# dbmate options
DATABASE_URL ?= "mysql://$(RDB_USER):$(RDB_PASS)@$(RDB_HOST):$(RDB_PORT)/$(RDB_NAME)"
DBMATE_MIGRATIONS_DIR ?= "schema/rdb/migrations"
DBMATE_SCHEMA_FILE ?= "schema/rdb/schema.sql"

MIGRATION_COMMENT ?= $(shell bash -c 'read -p "Comments: " pwd; echo $$pwd')

migrate-new:
	@DATABASE_URL=$(DATABASE_URL) dbmate -d $(DBMATE_MIGRATIONS_DIR) -s $(DBMATE_SCHEMA_FILE) new $(MIGRATION_COMMENT)

migrate-status:
	@DATABASE_URL=$(DATABASE_URL) dbmate -d $(DBMATE_MIGRATIONS_DIR) -s $(DBMATE_SCHEMA_FILE) status

## migrate-up: proceed db migration
migrate-up:
	@DATABASE_URL=$(DATABASE_URL) dbmate -d $(DBMATE_MIGRATIONS_DIR) -s $(DBMATE_SCHEMA_FILE) up

## migrate-down: rollback db migration
migrate-down:
	@DATABASE_URL=$(DATABASE_URL) dbmate -d $(DBMATE_MIGRATIONS_DIR) -s $(DBMATE_SCHEMA_FILE) down

## migrate-drop: drop database
migrate-drop:
	@DATABASE_URL=$(DATABASE_URL) dbmate -d $(DBMATE_MIGRATIONS_DIR) -s $(DBMATE_SCHEMA_FILE) drop

migrate-reset: migrate-drop migrate-up migrate-seed