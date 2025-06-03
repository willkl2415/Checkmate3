import re
import os
import json
import docx
import uuid
from docx.table import _Cell
from docx.text.paragraph import Paragraph
from typing import Union

from bs4 import BeautifulSoup

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
            yield docx.table.Table(child, parent)

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    text_blocks = []

    for block in iter_block_items(doc):
        if isinstance(block, Paragraph):
            text = get_text_from_paragraph(block)
            if text:
                text_blocks.append(text)
        elif isinstance(block, docx.table.Table):
            for row in block.rows:
                row_text = " | ".join(get_text_from_cell(cell) for cell in row.cells)
                if row_text:
                    text_blocks.append(row_text)

    return "\n".join(text_blocks)

def clean_text(text):
    """
    Removes Word-style footnote markers like [1], [12], etc.
    """
    return re.sub(r"\[\d{1,3}\]", "", text)

def chunk_text(text, max_chunk_size=800):
    paragraphs = text.split("\n")
    chunks = []
    current_chunk = ""

    for para in paragraphs:
        if not para.strip():
            continue

        if len(current_chunk) + len(para) + 1 <= max_chunk_size:
            current_chunk += "\n" + para if current_chunk else para
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = para

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

def extract_section_from_text(text):
    section_match = re.match(r"^\s*(\d+(\.\d+)*)(\s+|\.)(.*)", text)
    if section_match:
        return section_match.group(1).strip()
    return "Uncategorised"

def preprocess_document(file_path, max_chunk_size=800):
    raw_text = extract_text_from_docx(file_path)
    cleaned_text = clean_text(raw_text)
    paragraphs = cleaned_text.split("\n")

    chunks = []
    current_chunk = ""
    current_section = "Uncategorised"

    for para in paragraphs:
        if not para.strip():
            continue

        section = extract_section_from_text(para)
        if section != "Uncategorised":
            current_section = section

        if len(current_chunk) + len(para) + 1 <= max_chunk_size:
            current_chunk += "\n" + para if current_chunk else para
        else:
            if current_chunk:
                chunks.append({
                    "id": str(uuid.uuid4()),
                    "text": current_chunk.strip(),
                    "section": current_section
                })
            current_chunk = para

    if current_chunk:
        chunks.append({
            "id": str(uuid.uuid4()),
            "text": current_chunk.strip(),
            "section": current_section
        })

    return chunks

def save_chunks_to_json(chunks, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python preprocess_pipeline.py <input_docx_path> <output_json_path>")
        sys.exit(1)

    input_docx = sys.argv[1]
    output_json = sys.argv[2]

    chunks = preprocess_document(input_docx)
    save_chunks_to_json(chunks, output_json)
