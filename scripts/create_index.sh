#!/bin/sh

# Creates an index.html file in dist/ and each subdirectory
set -eu

cd "$1"
find . -type d -print -exec sh -c 'tree "$0" \
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
    -o "$0/index.html"' {} \;
