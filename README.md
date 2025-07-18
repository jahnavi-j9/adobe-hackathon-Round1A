# 🎯 Adobe India Hackathon 2025 – Connecting the Dots  
> *"Rethink Reading. Rediscover Knowledge."*

Welcome to our submission for the **Adobe India Hackathon 2025**.  
Our project transforms static PDFs into dynamic, intelligent documents — capable of understanding structure, surfacing insights, and connecting dots across knowledge sources — all offline.

<br>

## 🧠 Hackathon Overview

The hackathon consists of two technical rounds:

| Round       | Focus                                                   |
|-------------|----------------------------------------------------------|
| 🟦 **Round 1A** | Extract structured document outlines (Title, H1–H3)     |
| 🟩 **Round 1B** | Surface sections relevant to a specific persona         |

<br>

## ✨ Features Summary

| Feature                          | Status     |
|----------------------------------|------------|
| Extract Title, H1–H3 Headings    | ✅ Implemented |
| Font-size & Layout-based Logic   | ✅ Implemented |
| Structured JSON Output           | ✅ Yes      |
| Fully Offline (No Web Access)    | ✅ Yes      |
| CPU-Only Execution               | ✅ Yes      |
| Docker Support                   | ✅ Yes      |
| Sample Input/Output Provided     | ✅ Yes      |
| Multilingual PDF Support         | ⚙️ Planned  |

<br>

# 🟦 Round 1A – PDF Outline Extractor

## 📌 Objective

Automatically extract the **Title**, and **H1 / H2 / H3** headings with their corresponding page numbers from any PDF (≤ 50 pages), and output a valid JSON as per Adobe’s spec.

### ✅ Sample Output Format

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

<br>

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
│   └── config.py                # Thresholds/configs for heading detection
├── requirements.txt             # pdfplumber + PyMuPDF
├── Dockerfile                   # CPU-only, offline, AMD64-compliant
├── generate_dummy_pdf.py        # (Optional) Generate test PDFs with headings
├── sample.pdf                   # (Optional) A test input PDF
└── sample.json                  # (Optional) Expected output for sample.pdf
```

<br>

## 🧰 Tech Stack

| Tool/Library              | Use Case                         |
| ------------------------- | -------------------------------- |
| `pdfplumber`, `PyMuPDF`   | Parsing PDF text + layout        |
| `sentence-transformers`   | Semantic relevance ranking (R1B) |
| `scikit-learn`, `numpy`   | Similarity scoring, vector ops   |
| `transformers` (optional) | Summarization (R1B, optional)    |
| `Docker`                  | CPU-only, offline deployment     |
| `Python 3.10+`            | Primary language                 |

> 📌 All tools meet the offline, lightweight, and CPU-compliant constraints.

<br>

## ⚙️ How It Works (Round 1A)

1. **Place** `.pdf` files in the `app/input/` folder.

2. **Run the program:**

```bash
python src/main.py
```

3. It will:

* ✅ Extract title and headings (H1–H3)
* ✅ Save output JSON in `app/output/` with the same filename

<br>

## 📦 Dependencies

```
pdfplumber==0.10.2  
PyMuPDF==1.23.1
```

Install locally with:

```bash
pip install -r requirements.txt
```

<br>

## 🧠 Refined Heuristics for Heading Detection

Our system simulates how a human **visually parses** a document — not just scans font sizes. Here’s how we do it:

| #️⃣ | Heuristic Rule                                                                    | Signal Type      |
| --- | --------------------------------------------------------------------------------- | ---------------- |
| 1   | Title must appear in **top 15–25%** of page 0, based on Y-position                | Layout + Visual  |
| 2   | Font sizes are **ranked dynamically** per document (largest = H1)                 | Font Heuristic   |
| 3   | Headings must be **≤ 3 lines and ≤ 120 characters**                               | Content Filter   |
| 4   | **ALL CAPS or bold** text ≠ heading unless layout supports it                     | Visual + Context |
| 5   | Boost semantic phrases like `"Goals"`, `"Summary"`, `"Appendix"`                  | NLP + Semantics  |
| 6   | Skip content inside **tables, forms, QA blocks**                                  | Layout Heuristic |
| 7   | **Preserve section numbers** like `2.1 Mission` — never split/truncate            | Content Rule     |
| 8   | Merge **multi-line headings** only if alignment and spacing match                 | Visual Merge     |
| 9   | Prefer blocks with **white space padding above and below**                        | Structural Cue   |
| 10  | Skip **paragraph-like blocks** that appear bold but aren’t section-defining       | Noise Filter     |
| 11  | Repeated patterns (e.g., `"Step 1"`, `"Phase X"`) hint heading structure          | Pattern Learning |
| 12  | Promote early headings when **no clear H1 exists**, to prevent outline starvation | Recovery Logic   |
| 13  | Preserve all symbols/punctuation: no normalization (`Goals:`, not `Goals`)        | Output Policy    |
| 14  | Indented headings are allowed **if visually distinct & top-aligned**              | Layout Analysis  |
| 15  | Output must read like a **Table of Contents**, not just text with sizes           | UX-Oriented Rule |

<details>
<summary>🔍 View rules 16–35</summary>
<br>

| #️⃣ | Heuristic Rule                                                                    | Signal Type      |
| --- | --------------------------------------------------------------------------------- | ---------------- |
| 16  | Ignore headers/footers repeated across pages                                      | Layout Filter    |
| 17  | Remove text with high frequency + small font across pages                        | Noise Control    |
| 18  | Penalize left/right page margin-aligned content                                  | Layout Heuristic |
| 19  | Titles with no sibling block nearby are considered isolated → boost score        | Position Scoring |
| 20  | Headings often **follow white space**                                            | White Space Rule |
| 21  | Pages with no detected headings: fallback to top font chunks                     | Recovery Logic   |
| 22  | Prefer phrases with verbs/nouns over adjectives                                  | NLP Patterning   |
| 23  | Visually centered blocks on page 1 → strong title candidates                     | Title Heuristic  |
| 24  | Avoid text with large line-height                                                | Visual Check     |
| 25  | Penalize headings with **multiple font styles** in one line                      | Mixed Font Check |
| 26  | Limit each heading level to **≤ 30%** of total blocks                            | Balance Check    |
| 27  | Stop at **50 pages** even if file is larger                                      | Constraint Rule  |
| 28  | Avoid headings ending with ellipses/colons (unless list intro)                   | Punctuation Rule |
| 29  | Heading must be larger or bolder than adjacent text blocks                       | Contrast Rule    |
| 30  | Emphasize blocks that appear **only once** across document                       | Rarity Boost     |
| 31  | Prefer headings that appear **top-to-bottom sequentially**                       | Logical Flow     |
| 32  | Allow H2s inside H1s if indentation + size are justified                          | Nested Rule      |
| 33  | Penalize headings shorter than **3 characters**                                  | Min-Length Guard |
| 34  | Promote aligned blocks with white space above & followed by body text            | Composite Cue    |
| 35  | Use weighted ensemble of heuristics + layout scoring                             | Final Scoring    |

</details>



<br>

# 🟩 Round 1B – Persona-Driven Document Intelligence

### 🎯 Objective

Given:

* A **user persona**
* A **task**
* A **set of PDFs**

➡️ Surface and rank the **most relevant sections**, plus optionally summarize.

<br>

## 📥 Input/Output Example

```json
{
  "metadata": {
    "persona": "Undergraduate Chemistry Student",
    "job": "Prepare for reaction kinetics exam",
    "documents": ["doc1.pdf", "doc2.pdf"],
    "timestamp": "2025-07-16T18:30:00Z"
  },
  "sections": [
    {
      "document": "doc1.pdf",
      "page": 4,
      "section_title": "Reaction Mechanisms",
      "importance_rank": 1
    }
  ],
  "subsections": [
    {
      "document": "doc1.pdf",
      "page": 4,
      "refined_text": "The SN1 reaction involves a two-step mechanism..."
    }
  ]
}
```

<br>

## ⚙️ Planned Modules (Round 1B)

| File            | Description                            |
| --------------- | -------------------------------------- |
| `parser.py`     | Splits PDF into logical chunks         |
| `ranker.py`     | Ranks sections via semantic similarity |
| `summarizer.py` | Summarizes sections (optional)         |
| `main.py`       | Pipeline orchestrator                  |

<br>

## ✅ Round 1B Constraints Coverage

| Requirement       | ✅ Met |
| ----------------- | ----- |
| CPU-only          | ✅     |
| Offline execution | ✅     |
| ≤ 1GB model       | ✅     |
| Runtime ≤ 60s     | ✅     |
| Valid JSON Output | ✅     |

<br>

## 🐳 Docker Setup (Round 1A)

```bash
docker build --platform linux/amd64 -t round1a-extractor .

docker run --rm \
  -v $(pwd)/app/input:/app/input \
  -v $(pwd)/app/output:/app/output \
  --network none round1a-extractor
```

<br>

## 👥 Team DCODERZ

| Member  | Role                           |
| ------- | ------------------------------ |
| Jahnavi | Lead Developer                 |
| Sahithi | Document Intelligence Engineer |

📅 **July 2025**
🏁 **Adobe India Hackathon – Connecting the Dots**

<br>

## 📎 License

This project is licensed under the [MIT License](LICENSE).

<br>

> *"We don’t just extract — we understand. We don’t just read — we connect."*
> — Team DCODERZ
