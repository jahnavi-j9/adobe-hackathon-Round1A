import os
import json
from extractor import extract_outline, train_heading_model
from extractor import MLHeadingExtractor

# Automatically use absolute paths inside Docker, or relative paths locally
if os.path.exists("/app/input"):
    INPUT_DIR = "/app/input"
    OUTPUT_DIR = "/app/output"
else:
    INPUT_DIR = "app/input"
    OUTPUT_DIR = "app/output"

MODEL_PATH = "models/heading_model.pkl"
TRAIN_CSV_PATH = "training_data.csv"

def save_json(data, path):
    """Save the extracted JSON output to a given path."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def ensure_model_exists():
    """Train the model if it doesn't exist."""
    if not os.path.exists(MODEL_PATH):
        print(f"⚠️  Model not found at '{MODEL_PATH}'. Starting training from '{TRAIN_CSV_PATH}'.")
        if not os.path.exists(TRAIN_CSV_PATH):
            raise FileNotFoundError(f"❌ training_data.csv not found at {TRAIN_CSV_PATH}. Please label your training data.")
        
        # Train the model
        train_heading_model()
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"❌ Model training failed. Model still not found at '{MODEL_PATH}'.")
        print("✅ Model training complete!")

def process_all():
    """Process all PDFs in the input directory and output their outlines."""
    if not os.path.exists(INPUT_DIR):
        print(f"❌ Input folder '{INPUT_DIR}' not found. Please create it and add PDF files.")
        return

    files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(".pdf")]

    if not files:
        print(f"⚠️ No PDF files found in '{INPUT_DIR}'.")
        return

    # Ensure model is trained and ready
    ensure_model_exists()

    # Initialize the extractor (which loads the model)
    extractor = MLHeadingExtractor(model_path=MODEL_PATH)
    extractor.load_model()

    for f in files:
        pdf_path = os.path.join(INPUT_DIR, f)

        try:
            print(f"📄 Processing {f}...")
            result = extractor.extract_outline(pdf_path)
            print(f"   🔹 Title: {result['title'][:80]}")
            print(f"   🔹 Headings found: {len(result['outline'])}")
        except Exception as e:
            print(f"❌ Failed while processing {f}: {e}")
            continue

        output_filename = os.path.splitext(f)[0] + ".json"
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        save_json(result, output_path)
        print(f"✅ Output saved → {output_filename}\n")

if __name__ == "__main__":
    process_all()
