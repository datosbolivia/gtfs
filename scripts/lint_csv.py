#!/usr/bin/env python3
import argparse
import csv
import sys
from pathlib import Path

def process_file(file_path: Path, fix: bool) -> bool:
    """
    Process a CSV/GTFS text file to check or fix column ordering.
    Returns True if the file was/is valid (columns sorted), False if unsorted.
    """
    try:
        with open(file_path, mode="r", encoding="utf-8-sig", newline="") as f:
            content = f.read()
    except Exception as e:
        print(f"[ERROR] Could not read {file_path}: {e}", file=sys.stderr)
        return False

    if not content.strip():
        return True

    # Detect original newline style
    newline = "\r\n" if "\r\n" in content else "\n"
    lines = content.splitlines()

    reader = list(csv.reader(lines))
    if not reader:
        return True

    headers = reader[0]
    sorted_headers = sorted(headers)

    if headers == sorted_headers:
        return True

    if not fix:
        print(f"[FAIL] {file_path}")
        print(f"  Current: {', '.join(headers)}")
        print(f"  Sorted:  {', '.join(sorted_headers)}")
        return False

    # Fix mode: reorder headers and all rows
    sorted_indices = sorted(range(len(headers)), key=lambda i: headers[i])

    reordered_rows = []
    for row in reader:
        # Reorder row fields according to sorted header indices
        new_row = [row[i] if i < len(row) else "" for i in sorted_indices]
        reordered_rows.append(new_row)

    # Write reordered contents back to file
    with open(file_path, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, lineterminator=newline)
        writer.writerows(reordered_rows)

    print(f"[FIXED] {file_path}")
    return False


def main():
    parser = argparse.ArgumentParser(
        description="Lint and reorder CSV/GTFS file columns alphabetically."
    )
    parser.add_argument(
        "paths",
        nargs="*",
        default=["data"],
        help="Files or directories to check/fix (default: data/)",
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Automatically fix and reorder CSV columns in-place",
    )

    args = parser.parse_args()

    target_files = []
    for p in args.paths:
        path_obj = Path(p)
        if path_obj.is_file():
            if path_obj.suffix.lower() in (".txt", ".csv"):
                target_files.append(path_obj)
        elif path_obj.is_dir():
            for item in path_obj.rglob("*"):
                if item.is_file() and item.suffix.lower() in (".txt", ".csv"):
                    target_files.append(item)

    target_files = sorted(set(target_files))

    if not target_files:
        print("No CSV/GTFS files found to process.")
        sys.exit(0)

    unsorted_count = 0
    for file_path in target_files:
        is_ok = process_file(file_path, fix=args.fix)
        if not is_ok:
            unsorted_count += 1

    if args.fix:
        print(f"Done. Processed {len(target_files)} file(s). Fixed {unsorted_count} file(s).")
        sys.exit(0)
    else:
        if unsorted_count > 0:
            print(
                f"\nLint failed: {unsorted_count} of {len(target_files)} file(s) have unsorted columns."
            )
            print("Run 'python3 scripts/lint_csv.py --fix' or 'make fix-columns' to reorder columns automatically.")
            sys.exit(1)
        else:
            print(f"All {len(target_files)} file(s) have columns ordered alphabetically.")
            sys.exit(0)


if __name__ == "__main__":
    main()
