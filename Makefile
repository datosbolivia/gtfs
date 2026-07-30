all: build

create_gtfs:
	./scripts/create_gtfs.sh

create_indexes: create_gtfs
	./scripts/create_indexes.sh

build: create_indexes

# test: dist/index.html
# 	./scripts/test.sh

lint:
	python3 scripts/lint_csv.py

check-columns: lint

fix-columns:
	python3 scripts/lint_csv.py --fix

clean: ## Clean temporary files 
	rm -rf dist

.PHONY: all build clean create_gtfs create_indexes lint check-columns fix-columns
