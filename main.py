import os
import json
import fitz  # PyMuPDF
from typing import cast

INPUT_DIR = "//app//input"
OUTPUT_DIR = "//app//output"
print("RUNNING INSIDE DOCKER")
print("Current Working Directory:", os.getcwd())
print("INPUT_DIR is set to:", INPUT_DIR)

print("Checking for input directory at:", INPUT_DIR)
print("Host folder mapped to /app/input contains:", os.listdir(INPUT_DIR))


def get_outline_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    outline = []

    # Step 1: Try to get the title from first non-empty line of page 1
    title = "Untitled"
    try:
        page = cast(fitz.Page, doc[0])
        text_lines = page.get_text("text").strip().split('\n')
        for line in text_lines:
            if line.strip():
                title = line.strip()
                break
    except Exception as e:
        print(f"Could not extract title: {e}")

    # Step 2: Go through all pages and extract headings based on font size
    for page_num in range(len(doc)):
        page = cast(fitz.Page, doc[page_num])
        try:
            blocks = page.get_text("dict")["blocks"]
        except Exception as e:
            print(f"Could not parse page {page_num + 1}: {e}")
            continue

        for block in blocks:
            if "lines" not in block:
                continue
            for line in block["lines"]:
                spans = line.get("spans", [])
                if not spans:
                    continue
                text = " ".join([span["text"].strip() for span in spans]).strip()
                if not text or len(text) < 5:
                    continue

                font_size = max([span["size"] for span in spans])

                # Adjust font size thresholds as needed
                if font_size >= 18:
                    level = "H1"
                elif font_size >= 14:
                    level = "H2"
                elif font_size >= 11:
                    level = "H3"
                else:
                    continue  # Not a heading

                outline.append({
                    "level": level,
                    "text": text,
                    "page": page_num + 1
                })

    return {
        "title": title,
        "outline": outline
    }

def process_all_pdfs():
    if not os.path.exists(INPUT_DIR):
        print(f"Input directory not found: {INPUT_DIR}")
        return
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    for filename in os.listdir(INPUT_DIR):
        if filename.lower().endswith(".pdf"):
            input_path = os.path.join(INPUT_DIR, filename)
            output_path = os.path.join(OUTPUT_DIR, filename.replace(".pdf", ".json"))
            print(f"Processing: {filename}")
            outline = get_outline_from_pdf(input_path)

            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(outline, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    process_all_pdfs()
