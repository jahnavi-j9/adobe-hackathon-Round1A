import fitz  # PyMuPDF

MAX_HEADING_LENGTH = 120
MAX_HEADING_LINES = 3
TITLE_TOP_RATIO = 0.15  # Top 15% of page for H1 candidate

def is_form_like(lines):
    count = 0
    for line in lines:
        if len(line) < 40 and any(line.lstrip().startswith(str(n)) for n in range(1, 21)):
            count += 1
    return count >= 5

def extract_outline(doc):
    font_sizes = {}
    page_heights = []

    # Step 1: Collect all font sizes
    for page in doc:
        page_heights.append(page.rect.height)
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if block["type"] != 0:
                continue
            for line in block["lines"]:
                for span in line["spans"]:
                    size = round(span["size"], 1)
                    font_sizes[size] = font_sizes.get(size, 0) + 1

    sorted_sizes = sorted(font_sizes.items(), key=lambda x: -x[0])
    size_rank = {size: rank for rank, (size, _) in enumerate(sorted_sizes)}

    outline = []
    top_text_candidates = []

    for page_num, page in enumerate(doc):
        blocks = page.get_text("dict")["blocks"]
        page_lines_for_form_check = []

        for block in blocks:
            if block["type"] != 0:
                continue

            block_y = block.get("bbox", [0, 0, 0, 0])[1]
            lines = []
            fonts = set()

            for line in block["lines"]:
                text_line = ""
                for span in line["spans"]:
                    clean = span["text"].strip()
                    if not clean or len(clean) > MAX_HEADING_LENGTH:
                        continue
                    text_line += clean + " "
                    fonts.add(round(span["size"], 1))

                if text_line.strip():
                    lines.append(text_line.strip())
                    page_lines_for_form_check.append(text_line.strip())

            if not lines or len(lines) > MAX_HEADING_LINES:
                continue

            text = " ".join(lines).strip()
            if not text or len(text) > MAX_HEADING_LENGTH:
                continue

            font_size = max(fonts)
            rank = size_rank.get(font_size, 99)

            # Collect top-of-page H1 candidate from page 0
            if page_num == 0 and block_y < page_heights[0] * TITLE_TOP_RATIO:
                top_text_candidates.append((font_size, text, rank))

            # If form/table-like page, skip outline
            if is_form_like(page_lines_for_form_check):
                outline = []
                break

            # Allow H1–H3 for top 4 sizes
            rank_threshold = 4 if page_num == 0 else 3
            if rank > rank_threshold:
                continue

            level = f"H{rank + 1}"
            outline.append({
                "level": level,
                "text": text,
                "page": page_num
            })

    # Inject top-of-page H1 from page 0 if not already present
    if top_text_candidates:
        top_text_candidates.sort(reverse=True)
        top_text, top_rank = top_text_candidates[0][1], top_text_candidates[0][2]

        already_exists = any(h["text"] == top_text and h["page"] == 0 for h in outline)
        if not already_exists:
            outline.insert(0, {
                "level": "H1",
                "text": top_text,
                "page": 0
            })

    return {
        "title": "",
        "outline": outline
    }
