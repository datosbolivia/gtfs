#!/bin/sh

# Creates index.html for a single directory
set -eu

dir_path="${1:-.}"
cd "$dir_path"

tree . \
    -H "" \
    -L 1 \
    --noreport \
    --houtro "" \
    --dirsfirst \
    --charset utf-8 \
    -I "index.html" \
    -T "Community GTFS for Bolivia" \
    --ignore-case \
    --timefmt "%d-%b-%Y %H:%M" \
    -s \
    -D \
    -o index.html