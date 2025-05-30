import os
import random
import requests
import wikipedia
from docx import Document
from PyPDF2 import PdfReader, PdfWriter

# Define sensitive info pool
SENSITIVE_LINES = [
    "Credit Card: 4975592957335",
    "SSN: 123-45-6789",
    "Passport No: A12345678",
    "Phone: +62 812-3456-7890",
]

BASE_DIR = "sample_files"
MODIFIED_DIR = os.path.join(BASE_DIR, "modified")

def ensure_dirs():
    """Create all needed base and modified directories."""
    for folder in ["txt", "docx", "csv", "xlsx", "pdf"]:
        os.makedirs(os.path.join(BASE_DIR, folder), exist_ok=True)
        os.makedirs(os.path.join(MODIFIED_DIR, folder), exist_ok=True)

# Downloaders

def download_gutenberg_texts():
    ids = [1342, 1661]  # Pride and Prejudice, Sherlock Holmes
    for book_id in ids:
        url = f"https://www.gutenberg.org/files/{book_id}/{book_id}-0.txt"
        try:
            r = requests.get(url)
            r.raise_for_status()
            path = os.path.join(BASE_DIR, "txt", f"book_{book_id}.txt")
            with open(path, "w", encoding="utf-8") as f:
                f.write(r.text)
            print(f"[TXT] Downloaded book_{book_id}.txt")
        except Exception as e:
            print(f"[TXT] Failed to download {url} : {e}")

def create_docx_from_wikipedia():
    topics = ["Artificial intelligence", "Cloud computing"]
    for topic in topics:
        try:
            content = wikipedia.page(topic).content
            doc = Document()
            doc.add_heading(topic, 0)
            doc.add_paragraph(content[:5000])
            safe_name = topic.replace(" ", "_").replace("/", "_")
            path = os.path.join(BASE_DIR, "docx", f"{safe_name}.docx")
            doc.save(path)
            print(f"[DOCX] Created {safe_name}.docx")
        except Exception as e:
            print(f"[DOCX] Failed to create docx for {topic}: {e}")

def download_csv_files():
    urls = [
        "https://datahub.io/core/global-temp/r/annual.csv",
        "https://datahub.io/core/co2-fossil-global/r/global.csv"
    ]
    for i, url in enumerate(urls, 1):
        try:
            r = requests.get(url)
            r.raise_for_status()
            path = os.path.join(BASE_DIR, "csv", f"sample_{i}.csv")
            with open(path, "wb") as f:
                f.write(r.content)
            print(f"[CSV] Downloaded sample_{i}.csv")
        except Exception as e:
            print(f"[CSV] Failed to download {url} : {e}")

def download_xlsx_files():
    urls = [
        "https://datahub.io/core/gdp/r/gdp.xlsx",
        "https://datahub.io/core/finance-vix/r/finance-vix.xlsx"
    ]
    for i, url in enumerate(urls, 1):
        try:
            r = requests.get(url)
            r.raise_for_status()
            path = os.path.join(BASE_DIR, "xlsx", f"sample_{i}.xlsx")
            with open(path, "wb") as f:
                f.write(r.content)
            print(f"[XLSX] Downloaded sample_{i}.xlsx")
        except Exception as e:
            print(f"[XLSX] Failed to download {url} : {e}")

def download_pdf_files():
    urls = [
        "https://arxiv.org/pdf/2106.14806.pdf",
        "https://arxiv.org/pdf/2301.10226.pdf"
    ]
    for i, url in enumerate(urls, 1):
        try:
            r = requests.get(url)
            r.raise_for_status()
            path = os.path.join(BASE_DIR, "pdf", f"paper_{i}.pdf")
            with open(path, "wb") as f:
                f.write(r.content)
            print(f"[PDF] Downloaded paper_{i}.pdf")
        except Exception as e:
            print(f"[PDF] Failed to download {url} : {e}")

# Injection functions

def inject_into_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    insert_pos = random.randint(0, len(lines))
    sensitive_line = random.choice(SENSITIVE_LINES) + "\n"
    lines.insert(insert_pos, sensitive_line)
    new_path = os.path.join(MODIFIED_DIR, "txt", os.path.basename(file_path))
    with open(new_path, "w", encoding="utf-8") as f:
        f.writelines(lines)
    print(f"[TXT] Injected sensitive info into {os.path.basename(file_path)} at line {insert_pos + 1}")

def inject_into_docx(file_path):
    doc = Document(file_path)
    para_count = len(doc.paragraphs)
    insert_pos = random.randint(0, para_count)
    sensitive_line = random.choice(SENSITIVE_LINES)
    doc.add_paragraph("")  # Ensure at least one paragraph
    # Insert new paragraph at random position
    p = doc.paragraphs[insert_pos]
    p.insert_paragraph_before(sensitive_line)
    new_path = os.path.join(MODIFIED_DIR, "docx", os.path.basename(file_path))
    doc.save(new_path)
    print(f"[DOCX] Injected sensitive info into {os.path.basename(file_path)} at paragraph {insert_pos + 1}")

def inject_into_csv(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    insert_pos = random.randint(1, len(lines))  # avoid header line 0
    sensitive_line = random.choice(SENSITIVE_LINES) + "\n"
    lines.insert(insert_pos, sensitive_line)
    new_path = os.path.join(MODIFIED_DIR, "csv", os.path.basename(file_path))
    with open(new_path, "w", encoding="utf-8") as f:
        f.writelines(lines)
    print(f"[CSV] Injected sensitive info into {os.path.basename(file_path)} at line {insert_pos + 1}")

def inject_into_xlsx(file_path):
    # For XLSX, inject a new sheet with sensitive info (simpler than editing cells randomly)
    from openpyxl import load_workbook
    wb = load_workbook(file_path)
    sensitive_line = random.choice(SENSITIVE_LINES)
    ws = wb.create_sheet("Sensitive_Info")
    ws["A1"] = sensitive_line
    new_path = os.path.join(MODIFIED_DIR, "xlsx", os.path.basename(file_path))
    wb.save(new_path)
    print(f"[XLSX] Added sensitive info sheet into {os.path.basename(file_path)}")

def inject_into_pdf(file_path):
    try:
        reader = PdfReader(file_path)
        writer = PdfWriter()
        sensitive_line = random.choice(SENSITIVE_LINES)
        inserted = False

        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            # We'll add the sensitive line as a new page after a random page
            if not inserted and i == random.randint(0, len(reader.pages) - 1):
                # Insert a new page with the sensitive text
                from reportlab.pdfgen import canvas
                from reportlab.lib.pagesizes import letter
                from io import BytesIO

                packet = BytesIO()
                can = canvas.Canvas(packet, pagesize=letter)
                can.drawString(100, 750, sensitive_line)
                can.save()
                packet.seek(0)

                from PyPDF2 import PdfReader as PdfReader2
                new_pdf = PdfReader2(packet)
                writer.add_page(page)
                writer.add_page(new_pdf.pages[0])
                inserted = True
            else:
                writer.add_page(page)
        if not inserted:
            # fallback: just add a page with sensitive info at end
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import letter
            from io import BytesIO

            packet = BytesIO()
            can = canvas.Canvas(packet, pagesize=letter)
            can.drawString(100, 750, sensitive_line)
            can.save()
            packet.seek(0)

            from PyPDF2 import PdfReader as PdfReader2
            new_pdf = PdfReader2(packet)
            writer.add_page(new_pdf.pages[0])

        new_path = os.path.join(MODIFIED_DIR, "pdf", os.path.basename(file_path))
        with open(new_path, "wb") as f:
            writer.write(f)
        print(f"[PDF] Injected sensitive info into {os.path.basename(file_path)}")
    except Exception as e:
        print(f"[PDF] Failed to inject into {file_path}: {e}")

# Main flow

def main():
    print("Ensuring directories...")
    ensure_dirs()

    print("\nDownloading files...")
    download_gutenberg_texts()
    create_docx_from_wikipedia()
    download_csv_files()
    download_xlsx_files()
    download_pdf_files()

    print("\nStarting sensitive info injection...")
    # Map folder -> injection function
    injectors = {
        "txt": inject_into_txt,
        "docx": inject_into_docx,
        "csv": inject_into_csv,
        "xlsx": inject_into_xlsx,
        "pdf": inject_into_pdf,
    }

    for folder, injector in injectors.items():
        folder_path = os.path.join(BASE_DIR, folder)
        for fname in os.listdir(folder_path):
            file_path = os.path.join(folder_path, fname)
            try:
                injector(file_path)
            except Exception as e:
                print(f"[{folder.upper()}] Error injecting into {fname}: {e}")

    print("\nAll done!")

if __name__ == "__main__":
    main()
