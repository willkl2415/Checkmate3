import re
import os
import json
import uuid

DOCUMENT_NAME = "DTSM 2 Analysis of Individual Training 2023 Edition V1.0.txt"
MAX_PARAGRAPHS_PER_CHUNK = 3

INPUT_PATH = f"./docs/{DOCUMENT_NAME}"
OUTPUT_PATH = "./data/chunks.json"

SECTION_PATTERN = re.compile(r"^(\d+(?:\.\d+)*)(?:\s+)(.+)$")

def clean_text(text):
    return re.sub(r'\s+', ' ', text.strip())

def load_and_merge_headings(lines):
    """Handle lines like `2` followed by `Title` into `2 Title`."""
    merged_lines = []
    buffer = None
    for line in lines:
        if re.match(r"^\d+(\.\d+)*$", line.strip()):
            buffer = line.strip()
        elif buffer:
            if line.strip():
                merged_lines.append(f"{buffer} {line.strip()}")
                buffer = None
        else:
            merged_lines.append(line.strip())
    return merged_lines

def split_into_chunks(lines):
    chunks = []
    buffer = []
    current_section = None

    for line in lines:
        match = SECTION_PATTERN.match(line)
        if match:
            if buffer:
                chunks.append({
                    "id": str(uuid.uuid4()),
                    "document": DOCUMENT_NAME,
                    "section": current_section if current_section else "Uncategorised",
                    "content": " ".join(buffer)
                })
                buffer = []
            current_section = f"{match.group(1)} {match.group(2)}"
        elif current_section:
            buffer.append(clean_text(line))
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
            "section": current_section if current_section else "Uncategorised",
            "content": " ".join(buffer)
        })

    return chunks

def preprocess():
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        raw_lines = f.readlines()

    merged = load_and_merge_headings(raw_lines)
    chunks = split_into_chunks(merged)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    preprocess()
