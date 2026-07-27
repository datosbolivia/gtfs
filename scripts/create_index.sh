#!/bin/sh

# Creates an index.html file in dist/ and each subdirectory
set -eu

script_dir="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
target_dir="${1:-dist}"
cd "$target_dir"
find . -type d -print -exec "$script_dir/create_index_html.sh" {} \;
