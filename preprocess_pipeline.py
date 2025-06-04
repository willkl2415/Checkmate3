import os
import json
import re
import docx
import uuid
from docx.text.paragraph import Paragraph
from docx.table import _Cell
from typing import Union
from bs4 import BeautifulSoup

MAX_CHUNK_LENGTH = 1000
OVERLAP = 100

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

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    full_text = []
    for para in iter_block_items(doc):
        full_text.append(get_text_from_paragraph(para))
    return "\n".join(full_text)

def remove_footnotes(text):
    # Remove manually written footnote markers or definitions (basic heuristic)
    text = re.sub(r"\b\d{1,3}\b(?=\s[a-z])", "", text)
    text = re.sub(r"(Footnote|Note|Ref)[\s\d\-:]+.*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*\[\d{1,3}\]", "", text)
    return text

def split_into_chunks(text, max_length=MAX_CHUNK_LENGTH, overlap=OVERLAP):
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = min(start + max_length, len(words))
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += max_length - overlap
    return chunks

def extract_section(text):
    match = re.match(r"^(\d+(\.\d+)*)\s+", text.strip())
    return match.group(1) if match else "Uncategorised"

def clean_text(text):
    return re.sub(r"\s+", " ", text.strip())

def generate_chunks():
    output = []
    docs_path = "docs"
    for filename in os.listdir(docs_path):
        if not filename.endswith(".docx"):
            continue
        document_path = os.path.join(docs_path, filename)
        raw_text = extract_text_from_docx(document_path)
        scrubbed_text = remove_footnotes(raw_text)
        paragraphs = [p for p in scrubbed_text.split("\n") if p.strip()]
        buffer = ""
        for para in paragraphs:
            buffer += " " + para
            if len(buffer) > MAX_CHUNK_LENGTH:
                chunks = split_into_chunks(buffer)
                for chunk in chunks:
                    section = extract_section(chunk)
                    output.append({
                        "id": str(uuid.uuid4()),
                        "document": filename.replace(".docx", ""),
                        "section": section,
                        "content": clean_text(chunk)
                    })
                buffer = ""
        if buffer.strip():
            chunks = split_into_chunks(buffer)
            for chunk in chunks:
                section = extract_section(chunk)
                output.append({
                    "id": str(uuid.uuid4()),
                    "document": filename.replace(".docx", ""),
                    "section": section,
                    "content": clean_text(chunk)
                })

    os.makedirs("data", exist_ok=True)
    with open("data/chunks.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    generate_chunks()
