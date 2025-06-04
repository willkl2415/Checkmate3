# generate_chunks.py
import os
import json
import docx
import uuid
from bs4 import BeautifulSoup

INPUT_FOLDER = "docs"
OUTPUT_FILE = "data/chunks.json"
MAX_CHUNK_WORDS = 300

def clean_text(text):
    # Remove footnotes, empty lines, and strip
    text = text.replace("\xa0", " ").strip()
    text = BeautifulSoup(text, "html.parser").get_text()
    return " ".join(text.split())

def get_section_heading(paragraph_text):
    import re
    match = re.match(r"^(\d{1,2}(\.\d{1,2})*)\s+(.*)", paragraph_text)
    if match:
        return match.group(1), match.group(3)
    return None, None

def split_into_chunks(paragraphs):
    chunks = []
    current_chunk = []
    current_section = "Uncategorised"
    word_count = 0

    for para in paragraphs:
        text = clean_text(para.text)
        if not text:
            continue

        section_num, section_title = get_section_heading(text)
        if section_num:
            current_section = f"{section_num} {section_title}"
            continue

        current_chunk.append(text)
        word_count += len(text.split())

        if word_count >= MAX_CHUNK_WORDS:
            chunks.append(("\n".join(current_chunk), current_section))
            current_chunk = []
            word_count = 0

    if current_chunk:
        chunks.append(("\n".join(current_chunk), current_section))

    return chunks

def process_document(file_path, file_name):
    doc = docx.Document(file_path)
    chunks = split_into_chunks(doc.paragraphs)
    return [{
        "id": str(uuid.uuid4()),
        "document": file_name,
        "section": section,
        "content": content
    } for content, section in chunks]

def main():
    all_chunks = []
    for filename in os.listdir(INPUT_FOLDER):
        if filename.endswith(".docx"):
            file_path = os.path.join(INPUT_FOLDER, filename)
            print(f"Processing {filename}...")
            chunks = process_document(file_path, filename)
            all_chunks.extend(chunks)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2, ensure_ascii=False)
    print(f"Generated {len(all_chunks)} chunks.")

if __name__ == "__main__":
    main()
