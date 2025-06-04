# preprocess_pipeline.py
import os
import uuid
import json
import docx
from bs4 import BeautifulSoup
from docx.table import _Cell
from docx.text.paragraph import Paragraph
from typing import Union

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

def extract_text_and_sections(doc_path):
    doc = docx.Document(doc_path)
    paragraphs = []
    current_section = "Uncategorised"

    for para in iter_block_items(doc):
        text = para.text.strip()
        if not text:
            continue
        if text.lower().startswith("section") or text[:3].isdigit():
            current_section = text
        paragraphs.append((text, current_section))

    return paragraphs

def chunk_paragraphs(paragraphs, max_paragraphs=3):
    chunks = []
    current_chunk = []
    current_section = None

    for text, section in paragraphs:
        if current_section is None:
            current_section = section

        current_chunk.append(text)

        if len(current_chunk) == max_paragraphs:
            chunks.append({
                "id": str(uuid.uuid4()),
                "content": "\n\n".join(current_chunk),
                "section": current_section,
            })
            current_chunk = []
            current_section = None

    if current_chunk:
        chunks.append({
            "id": str(uuid.uuid4()),
            "content": "\n\n".join(current_chunk),
            "section": current_section or "Uncategorised",
        })

    return chunks
