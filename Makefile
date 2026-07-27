all: build

create_gtfs:
	./scripts/create_gtfs.sh dist

create_index: create_gtfs
	./scripts/create_index.sh dist

build: create_index

# test: dist/index.html
# 	./scripts/test.sh

clean: ## Clean temporary files 
	rm -rf dist

.PHONY: all build clean create_gtfs create_index
