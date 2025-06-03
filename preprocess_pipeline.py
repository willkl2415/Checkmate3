import os
import json
import uuid
import re

# === CONFIGURATION ===
INPUT_FILE = "docs/DTSM 2 Analysis of Individual Training 2023 Edition V1.0.txt"
OUTPUT_FILE = "data/chunks.json"
DOCUMENT_NAME = "DTSM 2 Analysis of Individual Training 2023 Edition V1.0"
MAX_PARAGRAPHS_PER_CHUNK = 3
SECTION_PATTERN = re.compile(r"^(\d{1,2}(?:\.\d{1,2})*)\s+(.+)$")  # e.g., 2.1 Introduction

# === LOAD AND CLEAN TEXT ===
def load_cleaned_paragraphs(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        raw_text = f.read()

    # Replace footnote markers like [1], [12], etc.
    cleaned = re.sub(r"\[\d+\]", "", raw_text)
    cleaned = re.sub(r"\s+", " ", cleaned)

    # Split on paragraph-like breaks
    paras = re.split(r"\n\s*\n", cleaned)
    return [p.strip() for p in paras if p.strip()]

# === CHUNKING LOGIC ===
def generate_chunks(paragraphs):
    chunks = []
    current_section = "Uncategorised"
    buffer = []

    for para in paragraphs:
        # If it looks like a heading, treat it as a section
        match = SECTION_PATTERN.match(para)
        if match:
            current_section = f"{match.group(1)} {match.group(2)}"
            continue

        buffer.append(para)
        if len(buffer) >= MAX_PARAGRAPHS_PER_CHUNK:
            chunks.append({
                "id": str(uuid.uuid4()),
                "document": DOCUMENT_NAME,
                "section": current_section,
                "content": " ".join(buffer)
            })
            buffer = []

    if buffer:
        chunks.append({
            "id": str(uuid.uuid4()),
            "document": DOCUMENT_NAME,
            "section": current_section,
            "content": " ".join(buffer)
        })

    return chunks

# === MAIN SCRIPT ===
def main():
    os.makedirs("data", exist_ok=True)
    paragraphs = load_cleaned_paragraphs(INPUT_FILE)
    chunks = generate_chunks(paragraphs)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
