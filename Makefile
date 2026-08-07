all: setup-hooks lint build validate-gtfs

setup-hooks:
	./scripts/install_hooks.sh

create_gtfs:
	./scripts/create_gtfs.sh

create_indexes: create_gtfs
	./scripts/create_indexes.sh

build: create_indexes

lint:
	python3 scripts/lint_gtfs_csv.py --check

check-columns: lint

fix-columns:
	python3 scripts/lint_gtfs_csv.py --fix

validate-gtfs: build
	./scripts/validate_gtfs.sh

clean: ## Clean temporary files 
	rm -rf dist .cache

.PHONY: all build clean create_gtfs create_indexes lint check-columns fix-columns validate-gtfs setup-hooks
