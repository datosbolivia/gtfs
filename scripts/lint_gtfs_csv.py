#!/usr/bin/env python3
"""
GTFS CSV Column Order and Formatting Script using gtfs_kit (https://github.com/mrcagney/gtfs_kit).
Enforces GTFS Schedule Reference canonical column ordering (https://gtfs.org/documentation/schedule/reference/)
and clean CSV formatting (LF line endings, UTF-8, no trailing spaces).
"""

import sys
import os
import io
import csv
import argparse
from pathlib import Path

try:
    import gtfs_kit as gk
except ImportError:
    print("Error: gtfs_kit library is not installed. Install with 'pip install gtfs-kit'.")
    sys.exit(1)

# Canonical GTFS Schedule Reference column order per https://gtfs.org/documentation/schedule/reference/
STANDARD_COLUMN_ORDER = {
    "agency.txt": [
        "agency_id", "agency_name", "agency_url", "agency_timezone",
        "agency_lang", "agency_phone", "agency_fare_url", "agency_email",
        "cemv_support"
    ],
    "stops.txt": [
        "stop_id", "stop_code", "stop_name", "tts_stop_name", "stop_desc",
        "stop_lat", "stop_lon", "zone_id", "stop_url", "location_type",
        "parent_station", "stop_timezone", "wheelchair_boarding", "level_id",
        "platform_code", "stop_access"
    ],
    "routes.txt": [
        "route_id", "agency_id", "route_short_name", "route_long_name",
        "route_desc", "route_type", "route_url", "route_color",
        "route_text_color", "route_sort_order", "continuous_pickup",
        "continuous_drop_off", "network_id", "cemv_support"
    ],
    "trips.txt": [
        "route_id", "service_id", "trip_id", "trip_headsign",
        "trip_short_name", "direction_id", "block_id", "shape_id",
        "wheelchair_accessible", "bikes_allowed", "cars_allowed",
        "safe_duration_factor", "safe_duration_offset"
    ],
    "stop_times.txt": [
        "trip_id", "arrival_time", "departure_time", "stop_id",
        "location_group_id", "location_id", "stop_sequence", "stop_headsign",
        "start_pickup_drop_off_window", "end_pickup_drop_off_window",
        "pickup_type", "drop_off_type", "continuous_pickup",
        "continuous_drop_off", "shape_dist_traveled", "timepoint",
        "pickup_booking_rule_id", "drop_off_booking_rule_id"
    ],
    "calendar.txt": [
        "service_id", "monday", "tuesday", "wednesday", "thursday",
        "friday", "saturday", "sunday", "start_date", "end_date"
    ],
    "calendar_dates.txt": [
        "service_id", "date", "exception_type"
    ],
    "fare_attributes.txt": [
        "fare_id", "price", "currency_type", "payment_method",
        "transfers", "agency_id", "transfer_duration"
    ],
    "fare_rules.txt": [
        "fare_id", "route_id", "origin_id", "destination_id", "contains_id"
    ],
    "timeframes.txt": [
        "timeframe_group_id", "start_time", "end_time", "service_id"
    ],
    "rider_categories.txt": [
        "rider_category_id", "rider_category_name", "is_default_fare_category",
        "eligibility_url"
    ],
    "fare_media.txt": [
        "fare_media_id", "fare_media_name", "fare_media_type"
    ],
    "fare_products.txt": [
        "fare_product_id", "fare_product_name", "rider_category_id",
        "fare_media_id", "amount", "currency"
    ],
    "fare_leg_rules.txt": [
        "leg_group_id", "network_id", "from_area_id", "to_area_id",
        "from_timeframe_group_id", "to_timeframe_group_id", "fare_product_id",
        "rule_priority"
    ],
    "fare_leg_join_rules.txt": [
        "from_network_id", "to_network_id", "from_stop_id", "to_stop_id"
    ],
    "fare_transfer_rules.txt": [
        "from_leg_group_id", "to_leg_group_id", "transfer_count",
        "duration_limit", "duration_limit_type", "fare_transfer_type",
        "fare_product_id"
    ],
    "areas.txt": [
        "area_id", "area_name"
    ],
    "stop_areas.txt": [
        "area_id", "stop_id"
    ],
    "networks.txt": [
        "network_id", "network_name"
    ],
    "route_networks.txt": [
        "network_id", "route_id"
    ],
    "shapes.txt": [
        "shape_id", "shape_pt_lat", "shape_pt_lon", "shape_pt_sequence",
        "shape_dist_traveled"
    ],
    "frequencies.txt": [
        "trip_id", "start_time", "end_time", "headway_secs", "exact_times"
    ],
    "transfers.txt": [
        "from_stop_id", "to_stop_id", "from_route_id", "to_route_id",
        "from_trip_id", "to_trip_id", "transfer_type", "min_transfer_time"
    ],
    "pathways.txt": [
        "pathway_id", "from_stop_id", "to_stop_id", "pathway_mode",
        "is_bidirectional", "length", "traversal_time", "stair_count",
        "max_slope", "min_width", "signposted_as", "reversed_signposted_as"
    ],
    "levels.txt": [
        "level_id", "level_index", "level_name"
    ],
    "location_groups.txt": [
        "location_group_id", "location_group_name"
    ],
    "location_group_stops.txt": [
        "location_group_id", "stop_id"
    ],
    "booking_rules.txt": [
        "booking_rule_id", "booking_type", "prior_notice_duration_min",
        "prior_notice_duration_max", "prior_notice_last_day",
        "prior_notice_last_time", "prior_notice_start_day",
        "prior_notice_start_time", "prior_notice_service_id", "message",
        "pickup_message", "drop_off_message", "phone_number", "info_url",
        "booking_url"
    ],
    "translations.txt": [
        "table_name", "field_name", "language", "translation",
        "record_id", "record_sub_id", "field_value"
    ],
    "feed_info.txt": [
        "feed_publisher_name", "feed_publisher_url", "feed_lang",
        "default_lang", "feed_start_date", "feed_end_date", "feed_version",
        "feed_contact_email", "feed_contact_url"
    ],
    "attributions.txt": [
        "attribution_id", "agency_id", "route_id", "trip_id",
        "organization_name", "is_producer", "is_operator", "is_authority",
        "attribution_url", "attribution_email", "attribution_phone"
    ]
}


def get_canonical_columns(filename: str, current_cols: list[str]) -> list[str]:
    """Returns headers ordered according to GTFS Schedule Reference, placing extra fields at the end."""
    standard_list = STANDARD_COLUMN_ORDER.get(filename, [])
    ordered = [c for c in standard_list if c in current_cols]
    extra = [c for c in current_cols if c not in ordered]
    ordered.extend(extra)
    return ordered


# Logical primary keys for sorting table rows
SORT_KEYS = {
    "stop_times.txt": ["trip_id", "stop_sequence"],
    "shapes.txt": ["shape_id", "shape_pt_sequence"],
    "stops.txt": ["stop_id"],
    "routes.txt": ["route_id"],
    "trips.txt": ["route_id", "service_id", "trip_id"],
    "agency.txt": ["agency_id"],
    "calendar.txt": ["service_id"],
    "calendar_dates.txt": ["service_id", "date"],
    "fare_attributes.txt": ["fare_id"],
    "fare_rules.txt": ["fare_id", "route_id"],
    "frequencies.txt": ["trip_id", "start_time"],
    "transfers.txt": ["from_stop_id", "to_stop_id"],
    "translations.txt": ["table_name", "field_name", "language", "record_id"],
}


def process_feed_dir(feed_dir: Path, fix: bool) -> bool:
    """Reads GTFS feed via gtfs_kit, cleans feed, enforces GTFS column ordering & clean CSV format."""
    print(f"Processing GTFS feed with gtfs_kit at: {feed_dir}")

    try:
        feed = gk.read_feed(feed_dir, dist_units='km')
        feed = feed.clean()
    except Exception as e:
        print(f"❌ Error loading feed at {feed_dir} with gtfs_kit: {e}")
        return False

    is_clean = True

    for txt_file in sorted(feed_dir.glob("*.txt")):
        filename = txt_file.name
        table_name = txt_file.stem
        df = getattr(feed, table_name, None)

        raw_existing = txt_file.read_text(encoding="utf-8-sig")

        if df is None or df.empty:
            rows = list(csv.reader(io.StringIO(raw_existing)))
            if not rows:
                continue
            original_cols = [c.strip() for c in rows[0]]
            target_cols = get_canonical_columns(filename, original_cols)
            col_map = [original_cols.index(c) for c in target_cols]

            out = io.StringIO()
            w = csv.writer(out, lineterminator="\n", quoting=csv.QUOTE_MINIMAL)
            w.writerow(target_cols)
            for r in rows[1:]:
                if not r or not any(cell.strip() for cell in r):
                    continue
                if len(r) < len(original_cols):
                    r.extend([""] * (len(original_cols) - len(r)))
                w.writerow([r[i] for i in col_map])
            formatted_csv = out.getvalue()
        else:
            original_cols = list(df.columns)
            target_cols = get_canonical_columns(filename, original_cols)
            df_reordered = df[target_cols].copy()

            # Ensure timepoint is non-empty if present
            if filename == "stop_times.txt" and "timepoint" in df_reordered.columns:
                df_reordered["timepoint"] = df_reordered["timepoint"].fillna(0).astype(int)

            # Sort rows by logical keys if present
            sort_cols = [c for c in SORT_KEYS.get(filename, []) if c in df_reordered.columns]
            if sort_cols:
                df_reordered = df_reordered.sort_values(by=sort_cols)

            out = io.StringIO()
            df_reordered.to_csv(out, index=False, lineterminator="\n", encoding="utf-8")
            formatted_csv = out.getvalue()
            # Clean up pandas NaN representation if any
            formatted_csv = formatted_csv.replace(",nan,", ",,").replace(",nan\n", ",\n")

        if raw_existing != formatted_csv:
            is_clean = False
            print(f"❌ [LINT ERROR] {txt_file.relative_to(feed_dir.parent.parent)}")
            print(f"   Original order:  {original_cols}")
            print(f"   Canonical order: {target_cols}")

            if fix:
                txt_file.write_text(formatted_csv, encoding="utf-8")
                print(f"   ✅ Reordered & formatted per GTFS spec: {filename}")
        else:
            print(f"✅ [OK] {txt_file.relative_to(feed_dir.parent.parent)}")

    return is_clean



def main():
    parser = argparse.ArgumentParser(description="Order and lint GTFS feed files using gtfs_kit and GTFS Schedule Reference.")
    parser.add_argument("--data-dir", default="data", help="Directory containing GTFS feeds (default: data)")
    parser.add_argument("--fix", action="store_true", help="Automatically sort and fix GTFS tables in-place")
    parser.add_argument("--check", action="store_true", help="Check column order and formatting")

    args = parser.parse_args()
    root_dir = Path(__file__).resolve().parent.parent
    data_dir = root_dir / args.data_dir

    feed_dirs = [d for d in data_dir.iterdir() if d.is_dir()]
    if not feed_dirs:
        print(f"No GTFS feed subdirectories found in {data_dir}")
        sys.exit(0)

    all_clean = True
    for fdir in feed_dirs:
        clean = process_feed_dir(fdir, fix=args.fix)
        if not clean:
            all_clean = False

    if not all_clean and not args.fix:
        print("\n❌ GTFS CSV lint errors found! Run 'python3 scripts/lint_gtfs_csv.py --fix' or 'make fix-columns' to fix.")
        sys.exit(1)
    elif not all_clean and args.fix:
        print("\n✨ All GTFS feeds successfully processed and formatted!")
    else:
        print("\n🎉 All GTFS feeds adhere to GTFS Schedule Reference column ordering and sorting!")


if __name__ == "__main__":
    main()
