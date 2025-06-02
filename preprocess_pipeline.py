# preprocess_pipeline.py

import os
import json
import re
from docx import Document
from nltk.tokenize import sent_tokenize

# Load ToC map automatically from toc_map.json
with open("toc_map.json", "r", encoding="utf-8") as f:
    toc_map = json.load(f)

def extract_text_from_docx(docx_path):
    doc = Document(docx_path)
    full_text = []
    for para in doc.paragraphs:
        text = para.text.strip()
        if text:
            full_text.append(text)
    return "\n".join(full_text)

def remove_footnotes(text):
    # Remove common footnote patterns like [1], [12], etc.
    return re.sub(r"\[\d+\]", "", text)

def split_into_chunks(text, chunk_size=3):
    sentences = sent_tokenize(text)
    chunks = []
    chunk = []
    for sentence in sentences:
        if len(chunk) < chunk_size:
            chunk.append(sentence)
        else:
            chunks.append(" ".join(chunk))
            chunk = [sentence]
    if chunk:
        chunks.append(" ".join(chunk))
    return chunks

def get_section_title(paragraph, toc_entries):
    for entry in toc_entries:
        if paragraph.startswith(entry):
            return entry
    return None

def tag_chunks_with_sections(text, toc_entries):
    paragraphs = text.split('\n')
    current_section = "Uncategorised"
    tagged_chunks = []

    for para in paragraphs:
        section_title = get_section_title(para, toc_entries)
        if section_title:
            current_section = section_title
        tagged_chunks.append((current_section, para))
    return tagged_chunks

def process_docx(docx_filename):
    docx_path = os.path.join("docs", docx_filename)
    document_name = os.path.splitext(docx_filename)[0]

    if docx_filename not in toc_map:
        print(f"[Warning] No ToC mapping found for {docx_filename}")
        toc_entries = []
    else:
        toc_entries = toc_map[docx_filename]

    raw_text = extract_text_from_docx(docx_path)
    clean_text = remove_footnotes(raw_text)
    tagged_paragraphs = tag_chunks_with_sections(clean_text, toc_entries)

    final_chunks = []
    buffer = []
    current_section = "Uncategorised"

    for section, paragraph in tagged_paragraphs:
        if section != current_section or len(buffer) >= 3:
            if buffer:
                final_chunks.append({
                    "document": document_name,
                    "section": current_section,
                    "content": " ".join(buffer)
                })
                buffer = []
        current_section = section
        buffer.append(paragraph)

    if buffer:
        final_chunks.append({
            "document": document_name,
            "section": current_section,
            "content": " ".join(buffer)
        })

    return final_chunks

def build_all_chunks(doc_folder="docs"):
    all_chunks = []
    for filename in os.listdir(doc_folder):
        if filename.endswith(".docx"):
            print(f"Processing: {filename}")
            chunks = process_docx(filename)
            all_chunks.extend(chunks)

    with open("data/chunks.json", "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, ensure_ascii=False, indent=2)
    print("✅ chunks.json has been generated with", len(all_chunks), "chunks.")

if __name__ == "__main__":
    build_all_chunks()

