all: build

create_gtfs:
	./scripts/create_gtfs.sh

create_indexes: create_gtfs
	./scripts/create_indexes.sh

build: create_indexes

# test: dist/index.html
# 	./scripts/test.sh

clean: ## Clean temporary files 
	rm -rf dist

.PHONY: all build clean create_gtfs create_indexes
