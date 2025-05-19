import os

file_path = "output/extended_financial_dataset.csv"  # Replace with your actual path

size_bytes = os.path.getsize(file_path)
size_mb = size_bytes / (1024 * 1024)  # Convert to megabytes
size_gb = size_bytes / (1024 ** 3)    # Convert to gigabytes

print(f"File size: {size_bytes} bytes")
print(f"File size: {size_mb:.2f} MB")
print(f"File size: {size_gb:.2f} GB")
