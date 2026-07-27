all: build

create_gtfs:
	./scripts/create_gtfs.sh

create_index: create_gtfs
	./scripts/create_index.sh

build: create_index

# test: dist/index.html
# 	./scripts/test.sh

clean: ## Clean temporary files 
	rm -rf dist

.PHONY: all build clean create_gtfs create_index
