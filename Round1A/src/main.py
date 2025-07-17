import os
import json
from extractor import extract_outline
from utils import load_pdf, write_json

INPUT_DIR = "/app/input"
OUTPUT_DIR = "/app/output"

def process_all_pdfs():
    for filename in os.listdir(INPUT_DIR):
        if filename.lower().endswith(".pdf"):
            filepath = os.path.join(INPUT_DIR, filename)
            print(f"Processing: {filename}")
            pdf = load_pdf(filepath)
            if not pdf:
                print(f"Failed to load: {filename}")
                continue

            output = extract_outline(pdf)
            output_filename = os.path.splitext(filename)[0] + ".json"
            write_json(output, os.path.join(OUTPUT_DIR, output_filename))
            print(f"Saved: {output_filename}")

if __name__ == "__main__":
    process_all_pdfs()
