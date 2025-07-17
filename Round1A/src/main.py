import os
import json
from extractor import extract_outline
from utils import write_json

# Auto-switch between local and Docker environment
RUNNING_LOCALLY = os.environ.get("ENV", "local") == "local"

if RUNNING_LOCALLY:
    INPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "app", "input")
    OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "app", "output")
else:
    INPUT_DIR = "/app/input"
    OUTPUT_DIR = "/app/output"

def process_all_pdfs():
    if not os.path.exists(INPUT_DIR):
        print(f"Input directory not found: {INPUT_DIR}")
        return

    for filename in os.listdir(INPUT_DIR):
        if filename.lower().endswith(".pdf"):
            filepath = os.path.join(INPUT_DIR, filename)
            print(f"Processing: {filename}")

            try:
                # Page count validation
                import pdfplumber
                with pdfplumber.open(filepath) as pdf:
                    if len(pdf.pages) > 50:
                        print(f"Skipped: {filename} has more than 50 pages")
                        continue

                # Run extraction
                output = extract_outline(filepath)
                output_filename = os.path.splitext(filename)[0] + ".json"
                output_path = os.path.join(OUTPUT_DIR, output_filename)
                write_json(output, output_path)
                print(f"Saved: {output_filename}")
            except Exception as e:
                print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    process_all_pdfs()
