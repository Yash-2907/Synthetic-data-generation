import os

def tail_csv_console(file_path, lines=20):
    with open(file_path, 'rb') as f:
        f.seek(0, os.SEEK_END)
        buffer = bytearray()
        pointer = f.tell()
        line_count = 0

        while pointer >= 0 and line_count < lines + 1:  # +1 in case last line is empty
            f.seek(pointer)
            byte = f.read(1)
            if byte == b'\n':
                line_count += 1
            buffer.extend(byte)
            pointer -= 1

        all_bytes = buffer[::-1]
        text = all_bytes.decode('utf-8', errors='ignore')
        rows = text.splitlines()[-lines:]

    print("\n📋 Last 20 lines of the CSV:\n")
    for i, row in enumerate(rows, 1):
        print(f"{i:2}: {row}")

# --- Change this to your actual file path ---
file_path = "benchmark_test/schema_2/schema_two_big.csv"

tail_csv_console(file_path)
