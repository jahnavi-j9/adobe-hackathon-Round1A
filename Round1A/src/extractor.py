import pdfplumber

def extract_outline(pdf):
    outline = []
    title = ""
    max_font_size = 0

    for page_num, page in enumerate(pdf.pages, start=1):
        words = page.extract_words(use_text_flow=True, keep_blank_chars=False)
        for word in words:
            text = word["text"].strip()
            size = float(word["size"])

            # Assume largest font on first page is the title
            if page_num == 1 and size > max_font_size:
                title = text
                max_font_size = size
                continue

            # Heuristic heading levels by font size (tune later)
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
