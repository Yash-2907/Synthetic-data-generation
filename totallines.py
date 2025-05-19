import csv

row_count = 0
with open("output/extended_financial_dataset.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    for _ in reader:
        row_count += 1

print(f"Total rows: {row_count}")
