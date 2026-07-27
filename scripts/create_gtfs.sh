#!/bin/sh

mkdir -p dist
echo "Community GTFS for Bolivia

This website contains GTFS feeds for Bolivia.

See https://github.com/datosbolivia/gtfs for more information." > dist/README.txt

# for now, only create a fake hierarchy
mkdir -p dist/miteleferico
