import os
import json
import uuid
import re
import docx
from docx.text.paragraph import Paragraph

# === CONFIGURATION ===
INPUT_FILE = "docs/DTSM 2 Analysis of Individual Training 2023 Edition V1.0.docx"
OUTPUT_FILE = "data/chunks.json"
DOCUMENT_NAME = "DTSM 2 Analysis of Individual Training 2023 Edition V1.0"
MAX_PARAGRAPHS_PER_CHUNK = 3
SECTION_PATTERN = re.compile(r"^(\d{1,2}(?:\.\d{1,2})*)\s+(.+)$")  # e.g., 2.1 Introduction

# === CLEAN TEXT ===
def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# === EXTRACT PARAGRAPHS ===
def extract_paragraphs_from_docx(file_path):
    doc = docx.Document(file_path)
    return [clean_text(p.text) for p in doc.paragraphs if p.text.strip()]

# === CHUNKING LOGIC ===
def generate_chunks(paragraphs):
    chunks = []
    current_section = None
    buffer = []
    section_started = False

    for para in paragraphs:
        match = SECTION_PATTERN.match(para)
        if match:
            if buffer:
                chunks.append({
                    "id": str(uuid.uuid4()),
                    "document": DOCUMENT_NAME,
                    "section": current_section if current_section else "Uncategorised",
                    "content": " ".join(buffer)
                })
                buffer = []

            current_section = match.group(1) + " " + match.group(2)
            section_started = True
            continue

        if not section_started:
            continue

        buffer.append(para)
        if len(buffer) >= MAX_PARAGRAPHS_PER_CHUNK:
            chunks.append({
                "id": str(uuid.uuid4()),
                "document": DOCUMENT_NAME,
                "section": current_section if current_section else "Uncategorised",
                "content": " ".join(buffer)
            })
            buffer = []

    if buffer:
        chunks.append({
            "id": str(uuid.uuid4()),
            "document": DOCUMENT_NAME,
            "section": current_section if current_section else "Uncategorised",
            "content": " ".join(buffer)
        })

    return chunks

# === MAIN SCRIPT ===
def main():
    os.makedirs("data", exist_ok=True)
    paragraphs = extract_paragraphs_from_docx(INPUT_FILE)
    chunks = generate_chunks(paragraphs)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
