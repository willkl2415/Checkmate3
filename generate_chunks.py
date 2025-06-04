# generate_chunks.py
import os
import json
from preprocess_pipeline import extract_text_and_sections, chunk_paragraphs

SOURCE_DIR = "docs"
OUTPUT_PATH = "data/chunks.json"
all_chunks = []

for filename in os.listdir(SOURCE_DIR):
    if filename.endswith(".docx"):
        doc_path = os.path.join(SOURCE_DIR, filename)
        print(f"⏳ Processing {filename}...")
        paragraphs = extract_text_and_sections(doc_path)
        chunks = chunk_paragraphs(paragraphs)
        for chunk in chunks:
            chunk["document"] = filename
        all_chunks.extend(chunks)

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(all_chunks, f, ensure_ascii=False, indent=2)

print(f"✅ chunks.json written with {len(all_chunks)} chunks from {SOURCE_DIR}")
