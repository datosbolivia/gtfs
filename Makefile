all: build validate-gtfs

create_gtfs:
	./scripts/create_gtfs.sh

create_indexes: create_gtfs
	./scripts/create_indexes.sh

build: create_indexes

validate-gtfs: build
	./scripts/validate_gtfs.sh

clean: ## Clean temporary files 
	rm -rf dist .cache

.PHONY: all build clean create_gtfs create_indexes validate-gtfs
