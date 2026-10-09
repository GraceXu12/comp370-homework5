import csv
from collections import defaultdict
from datetime import datetime

input_file = "311_Service_Requests_from_2010_to_Present_20250928.csv"
output_file = "preprocessed_311_monthly.csv"

totals = defaultdict(lambda: [0.0, 0])
overall_totals = defaultdict(lambda: [0.0, 0])


with open(input_file, mode="r", encoding="utf-8") as f:
    reader = csv.reader(f)

    header = next(reader)
    col_map = {col.strip(): idx for idx, col in enumerate(header)}

    created_idx = col_map.get("Created Date")
    closed_idx = col_map.get("Closed Date")
    zip_idx = col_map.get("Incident Zip")

    for row_num, row in enumerate(reader, start=1):
        try:
            created_str = row[created_idx].strip()
            closed_str = row[closed_idx].strip()
            zip_str = row[zip_idx].strip()

            # skip if zip code is missing 
            if not zip_str:
                continue

            # format zip code 
            zip_code = (
                zip_str.split(".")[0].zfill(5)[:5]
                if zip_str.split(".")[0].isdigit()
                else zip_str[:5])

            # Skip if closed date missing
            if not closed_str:
                continue

            # adjust format string if different date format
            created_dt = datetime.strptime(
                created_str, "%m/%d/%Y %I:%M:%S %p"
            )
            closed_dt = datetime.strptime(closed_str, "%m/%d/%Y %I:%M:%S %p")

            # opened in 2020 
            if created_dt.year != 2024:
                continue

            # duration in hours 
            duration_hours = (
                closed_dt - created_dt
            ).total_seconds() / 3600.0

            # skip negative response times 
            if duration_hours < 0:
                continue

            # month from closed date 
            closed_month = closed_dt.month

            # accumulate totals for zipcode and overall
            totals[(zip_code, closed_month)][0] += duration_hours
            totals[(zip_code, closed_month)][1] += 1

            overall_totals[closed_month][0] += duration_hours
            overall_totals[closed_month][1] += 1

        except (ValueError, IndexError):
            continue


with open(output_file, mode="w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Incident Zip", "closed_month", "response_time_hours"])

    for (zip_code, month), (total_hrs, count) in totals.items():
        if count > 0:
            writer.writerow([zip_code, month, total_hrs / count])

    for month, (total_hrs, count) in overall_totals.items():
        if count > 0:
            writer.writerow(["ALL", month, total_hrs / count])

print(f"saved to {output_file}")