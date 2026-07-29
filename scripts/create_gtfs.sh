#!/bin/sh

set -e

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
ROOT_DIR=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)
DIST_DIR="$ROOT_DIR/dist"
DATA_DIR="$ROOT_DIR/data"

mkdir -p "$DIST_DIR"
echo "Community GTFS for Bolivia

This website contains GTFS feeds for Bolivia.

See https://github.com/datosbolivia/gtfs for more information." > "$DIST_DIR/README.txt"

# Directories to process. Only mi-teleferico is included for now.
directories="mi-teleferico"

for directory in $directories; do
  source_dir="$DATA_DIR/$directory"
  archive_path="$DIST_DIR/${directory}.zip"

  if [ -d "$source_dir" ]; then
    (cd "$source_dir" && zip -j "$archive_path" *.txt >/dev/null)
  fi
done
