import os
import json
import uuid
import re
import docx
from docx.table import _Cell
from docx.text.paragraph import Paragraph
from typing import Union

# === CONFIGURATION ===
INPUT_FILE = "docs/JSP 822 V7.0 Vol 2 V3.0 Defence Individual Training.docx"
OUTPUT_FILE = "data/chunks.json"
DOCUMENT_NAME = "JSP 822 V7.0 Vol 2 V3.0 Defence Individual Training"
MAX_PARAGRAPHS_PER_CHUNK = 3
SECTION_PATTERN = re.compile(r"^(\d{1,2}(?:\.\d{1,2})*)\s+(.+)$")

# === UTILITIES ===
def get_text_from_paragraph(paragraph):
    return paragraph.text.strip()

def get_text_from_cell(cell):
    return "\n".join(get_text_from_paragraph(p) for p in cell.paragraphs)

def iter_block_items(parent):
    if isinstance(parent, docx.document.Document):
        parent_elm = parent._element.body
    elif isinstance(parent, _Cell):
        parent_elm = parent._tc
    else:
        raise ValueError("Unsupported parent type")

    for child in parent_elm.iterchildren():
        if child.tag.endswith('}p'):
            yield Paragraph(child, parent)
        elif child.tag.endswith('}tbl'):
            yield child

# === CLEAN TEXT + FOOTNOTE SCRUBBER ===
def clean_text(text: str) -> str:
    text = re.sub(r"\[\d+\]", "", text)  # footnote markers
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# === PARAGRAPH EXTRACTOR ===
def load_paragraphs_from_docx(doc_path):
    doc = docx.Document(doc_path)
    paragraphs = []
    for block in iter_block_items(doc):
        if isinstance(block, Paragraph):
            cleaned = clean_text(block.text)
            if cleaned:
                paragraphs.append(cleaned)
    return paragraphs

# === CHUNKING FUNCTION ===
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
            current_section = f"{match.group(1)} {match.group(2)}"
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

# === MAIN ===
def main():
    os.makedirs("data", exist_ok=True)
    paragraphs = load_paragraphs_from_docx(INPUT_FILE)
    chunks = generate_chunks(paragraphs)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
