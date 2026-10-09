import argparse
import csv
from datetime import datetime
import sys

def parse_date(date):
    if "-" in date:
        return datetime.strptime(date, "%Y-%m-%d")
    return datetime.strptime(date, "%m/%d/%Y")

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", required=True)
parser.add_argument("-s", "--start_date", required=True)
parser.add_argument("-e", "--end_date", required=True)
parser.add_argument("-o", "--output")
args = parser.parse_args()

start = parse_date(args.start_date)
end = parse_date(args.end_date)
counts = {}

with open(args.input, "r", encoding="utf-8", errors="replace") as f:
    reader = csv.DictReader(f)

    for row in reader:
        created = row["Created Date"].strip()

        if not created:
            continue

        try:
            date = parse_date(created.split()[0])
        except ValueError:
            continue

        if start <= date <= end:
            complaint = row["Complaint Type"].strip()
            borough = row["Borough"].strip()
            key = (complaint, borough)

            counts[key] = counts.get(key, 0) + 1

# Write results
if args.output:
    output = open(args.output, "w", newline="", encoding="utf-8")
else:
    output = sys.stdout

writer = csv.writer(output)
writer.writerow(["complaint_type", "borough", "count"])

for (complaint, borough), count in sorted(counts.items()):
    writer.writerow([complaint, borough, count])

if args.output:
    output.close()
