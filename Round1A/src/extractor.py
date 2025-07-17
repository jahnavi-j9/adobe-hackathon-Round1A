import fitz  # PyMuPDF

def extract_outline(pdf_path):
    doc = fitz.open(pdf_path)
    outline = []
    title = ""
    max_font_size = 0

    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" not in block:
                continue
            for line in block["lines"]:
                for span in line["spans"]:
                    text = span["text"].strip()
                    if not text:
                        continue

                    size = span["size"]

                    # Set title as largest text on first page
                    if page_num == 1 and size > max_font_size:
                        title = text
                        max_font_size = size
                        continue

                    # Heading classification
                    if size >= 16:
                        level = "H1"
                    elif size >= 14:
                        level = "H2"
                    elif size >= 12:
                        level = "H3"
                    else:
                        continue

                    outline.append({
                        "level": level,
                        "text": text,
                        "page": page_num
                    })

    return {
        "title": title,
        "outline": outline
    }
