#!/usr/bin/env bash

set -e

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
ROOT_DIR=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)
DIST_DIR="$ROOT_DIR/dist"
CACHE_DIR="$ROOT_DIR/.cache"
VALIDATOR_JAR="$CACHE_DIR/gtfs-validator.jar"
VALIDATOR_VERSION="8.0.1"
VALIDATOR_URL="https://github.com/MobilityData/gtfs-validator/releases/download/v${VALIDATOR_VERSION}/gtfs-validator-${VALIDATOR_VERSION}-cli.jar"

mkdir -p "$CACHE_DIR"
mkdir -p "$DIST_DIR/validation_reports"

# 1. Download GTFS validator CLI jar if not already cached
if [ ! -f "$VALIDATOR_JAR" ]; then
    echo "Downloading MobilityData GTFS Validator v${VALIDATOR_VERSION}..."
    curl -sSL -o "$VALIDATOR_JAR" "$VALIDATOR_URL"
    echo "Downloaded GTFS Validator jar to $VALIDATOR_JAR"
fi

# 2. Check if Java is available
if ! command -v java >/dev/null 2>&1; then
    echo "Error: Java runtime (JRE/JDK) is required to run MobilityData GTFS Validator."
    exit 1
fi

# 3. Find GTFS zip files in dist directory
gtfs_zips=("$DIST_DIR"/*.zip)

if [ ${#gtfs_zips[@]} -eq 0 ] || [ ! -f "${gtfs_zips[0]}" ]; then
    echo "No GTFS zip files found in $DIST_DIR. Running 'make build'..."
    make -C "$ROOT_DIR" build
    gtfs_zips=("$DIST_DIR"/*.zip)
fi

echo "=========================================="
echo " Running GTFS Schedule Validator"
echo "=========================================="

HAS_ERRORS=0

for zip_file in "${gtfs_zips[@]}"; do
    if [ -f "$zip_file" ]; then
        feed_name=$(basename "$zip_file" .zip)
        output_report_dir="$DIST_DIR/validation_reports/$feed_name"
        mkdir -p "$output_report_dir"

        echo "Validating feed: $feed_name ($zip_file)..."
        
        java -jar "$VALIDATOR_JAR" \
            --input "$zip_file" \
            --output_base "$output_report_dir" \
            --country_code BO

        report_json="$output_report_dir/report.json"
        if [ -f "$report_json" ]; then
            error_count=$(grep -o '"severity":"ERROR"' "$report_json" | wc -l || true)
            warning_count=$(grep -o '"severity":"WARNING"' "$report_json" | wc -l || true)
            echo "Report generated for $feed_name: $error_count Error(s), $warning_count Warning(s)."
            echo "HTML report available at: $output_report_dir/report.html"
            
            if [ "$error_count" -gt 0 ]; then
                HAS_ERRORS=1
            fi
        fi
        echo "------------------------------------------"
    fi
done

if [ "$HAS_ERRORS" -ne 0 ]; then
    echo "❌ GTFS Validation completed with ERRORS!"
    exit 1
else
    echo "🎉 GTFS Validation completed successfully!"
fi
