import os
import fitz  # PyMuPDF
import json
from src.extractor import extract_outline

INPUT_DIR = "app/input"
OUTPUT_DIR = "app/output"

def process_pdf(file_path):
    try:
        doc = fitz.open(file_path)
        return doc
    except Exception as e:
        print(f"Failed to open PDF: {file_path}\nError: {e}")
        return None

def save_json(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def process_all():
    files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(".pdf")]

    for f in files:
        pdf_path = os.path.join(INPUT_DIR, f)
        doc = process_pdf(pdf_path)
        if not doc:
            continue

        result = extract_outline(doc)
        doc.close()

        output_filename = os.path.splitext(f)[0] + ".json"
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        save_json(result, output_path)

        print(f"Processed {f} → {output_filename}")

if __name__ == "__main__":
    process_all()
