
# Round 1A – PDF Outline Extractor

This module extracts structured outlines from PDFs for the Adobe India Hackathon 2025 – "Connecting the Dots" Challenge.

## 📌 Objective

Automatically extract the **Title**, and **H1 / H2 / H3 headings** with their corresponding page numbers from any PDF (≤ 50 pages), and output a valid JSON format as specified.

### ✅ Output Example

```json
{
  "title": "Understanding AI",
  "outline": [
    { "level": "H1", "text": "Introduction", "page": 1 },
    { "level": "H2", "text": "What is AI?", "page": 2 },
    { "level": "H3", "text": "History of AI", "page": 3 }
  ]
}
````



## 📂 Folder Structure

```
Round1A/
├── app/
│   ├── input/                   # Input PDFs placed here (Docker-mounted)
│   └── output/                  # Output JSONs written here (Docker-mounted)
├── src/
│   ├── main.py                  # Entrypoint for processing all PDFs
│   ├── extractor.py             # Extracts title, H1, H2, H3 using font sizes
│   ├── utils.py                 # Helpers for reading PDF, writing JSON
│   └── config.py                # (Optional) Thresholds/configs for heading detection
├── requirements.txt             # pdfplumber + PyMuPDF
├── Dockerfile                   # CPU-only, offline, AMD64-compliant
├── generate_dummy_pdf.py        # (Optional) Generate test PDFs with headings
├── sample.pdf                   # (Optional) A test input PDF
└── sample.json                  # (Optional) Expected output for sample.pdf

```



## 📦 Dependencies

```txt
pdfplumber==0.10.2
PyMuPDF==1.23.1
```

Install locally with:

```bash
pip install -r requirements.txt
```




## ⚙️ How It Works

1. **Place** `.pdf` files into the `app/input/` directory.

2. **Run the program**:

   ```bash
   python src/main.py
   ```

3. The script will:

   * ✅ Open each PDF file
   * ✅ Extract the **title** and **headings (H1, H2, H3)** using font-size heuristics
   * ✅ Generate a `.json` file with structured output
   * ✅ Save the output to the `app/output/` folder with the same filename as the input PDF

4. The solution is:

   * ⚙️ Fully **offline**
   * 💻 **CPU-only**
   * 📁 Compatible with Adobe’s expected input/output schema
   * 🚀 Modular and reusable for Round 1B and Round 2



## 🚀 Progress Tracker

* [x] Folder structure
* [x] Heading extraction logic
* [x] JSON output format
* [x] GitHub commit history setup
* [ ] Dockerfile for AMD64 CPU-based offline execution
* [ ] Performance tuning and multilingual handling
* [ ] Final sample testing and benchmarking
* [ ] Round 2 integration




## 👤 Authors

Team: DCODERZ  
Members:  
- Jahnavi  
- Sahithi   

Date: July 2025  
Hackathon: Adobe India Hackathon – Connecting the Dots




