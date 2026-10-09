import argparse
import csv
from datetime import datetime
import sys


def parse_date(date_str: str) -> datetime:
    """Parses date string formatted as YYYY-MM-DD or MM/DD/YYYY."""
    fmt = "%Y-%m-%d" if "-" in date_str else "%m/%d/%Y"
    return datetime.strptime(date_str, fmt)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True, type=str)
    parser.add_argument("-s", "--start_date", required=True, type=str)
    parser.add_argument("-e", "--end_date", required=True, type=str)
    parser.add_argument("-o", "--output", type=str)
    args = parser.parse_args()

    start_date = parse_date(args.start_date)
    end_date = parse_date(args.end_date)
    counts = {}

    with open(args.input, "r", encoding="utf-8", errors="replace") as f:
        for row in csv.DictReader(f):
            created = row.get("Created Date", "").strip()
            if not created:
                continue

            try:
                date = parse_date(created.split()[0])
            except ValueError:
                continue

            if start_date <= date <= end_date:
                complaint = row.get("Complaint Type", "Unspecified").strip()
                borough = row.get("Borough", "Unspecified").strip()
                counts[(complaint, borough)] = counts.get((complaint, borough), 0) + 1
    
    if args.output:
        out_stream = open(args.output, "w", newline="", encoding="utf-8")
    else:
        out_stream = sys.stdout

    try:
        writer = csv.writer(out_stream)
        writer.writerow(["complaint_type", "borough", "count"])
        for (complaint, borough), count in sorted(counts.items()):
            writer.writerow([complaint, borough, count])
    finally:
        if args.output:
            out_stream.close()


if __name__ == "__main__":
    main()