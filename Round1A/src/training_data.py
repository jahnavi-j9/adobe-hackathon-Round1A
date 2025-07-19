from typing import List
import fitz  # PyMuPDF
import pandas as pd
import numpy as np
import os
from extractor import MLHeadingExtractor

def create_training_data(pdf_paths: List[str], output_path: str):
    """Create training dataset from sample PDFs with clearer tabular structure"""
    
    extractor = MLHeadingExtractor()
    all_features = []
    
    for pdf_path in pdf_paths:
        if not os.path.exists(pdf_path):
            print(f"⚠️ PDF not found: {pdf_path}")
            continue
            
        print(f"📄 Processing {pdf_path}...")
        doc = fitz.open(pdf_path)
        features = extractor.extract_text_features(doc)

        for feat in features:
            # Assign default label to be updated manually later
            feat['label'] = 'Body'
        
        all_features.extend(features)
        doc.close()
        print(f"✅ Extracted {len(features)} text elements from {pdf_path}")
    
    if not all_features:
        print("❌ No features extracted. Exiting.")
        return

    # Clean & reorder columns for better readability
    df = pd.DataFrame(all_features)

    # Put "interesting" fields first
    column_order = [
        "text",                                # Actual text
        "font_size", "is_bold", "is_italic",   # Style info
        "page",                                # Page number
        "cap_ratio", "line_length", "word_count",  # Text stats
        "x_pos_norm", "y_pos_norm",            # Position on page
        "relative_font_size", "indentation",   # Layout clues
        "starts_with_number", "ends_with_colon", "all_caps",  # Heuristic clues
        "vertical_spacing_above", "vertical_spacing_below",   # Spacing to neighbors
        "label"                                # The label you will assign
    ]

    # Only include columns that exist in the dataframe
    column_order = [col for col in column_order if col in df.columns]
    df = df[column_order]

    # Save CSV
    dirpath = os.path.dirname(output_path)
    if dirpath:
        os.makedirs(dirpath, exist_ok=True)
    
    df.to_csv(output_path, index=False)
    print(f"\n📁 Training data saved to: {output_path}")
    print(f"📝 Please manually update the 'label' column with: Title, H1, H2, H3, or Body")
    print(f"🔍 Total rows: {len(df)}")

def main():
    input_dir = "app/input"
    output_path = "training_data.csv"

    if not os.path.exists(input_dir):
        print(f"❌ Input directory '{input_dir}' not found!")
        return
    
    pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith(".pdf")]
    if not pdf_files:
        print(f"❌ No PDF files found in '{input_dir}'")
        return

    pdf_paths = [os.path.join(input_dir, f) for f in pdf_files]
    print(f"🔍 Found {len(pdf_files)} PDF files:")
    for pdf in pdf_files:
        print(f"   - {pdf}")

    create_training_data(pdf_paths, output_path)

if __name__ == "__main__":
    main()
