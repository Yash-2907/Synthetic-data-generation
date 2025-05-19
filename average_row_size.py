sample_size = 1000
total_bytes = 0

with open("D:/fortii/output/extended_financial_dataset.csv", "r", encoding="utf-8") as f:
    for i in range(sample_size):
        line = f.readline()
        total_bytes += len(line)

avg_row_size = total_bytes / sample_size
print(f"Average row size: {avg_row_size:.2f} bytes")
