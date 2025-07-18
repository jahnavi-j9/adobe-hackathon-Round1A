import pdfplumber
import json

def load_pdf(path):
    try:
        return pdfplumber.open(path)
    except Exception as e:
        print(f"Error loading PDF: {e}")
        return None

def write_json(data, path):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error writing JSON: {e}")
