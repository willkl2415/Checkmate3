import os
import json
from docx import Document

docs_path = "docs"
output_file = "chunks.json"
chunks = []

def extract_paragraphs(doc_path, doc_name):
    document = Document(doc_path)
    current_heading = ""
    for para in document.paragraphs:
        text = para.text.strip()
        if not text:
            continue
        if para.style.name.startswith("Heading"):
            current_heading = text
        else:
            chunks.append({
                "document": doc_name,
                "heading": current_heading,
                "content": text
            })

for filename in os.listdir(docs_path):
    if filename.endswith(".docx"):
        doc_path = os.path.join(docs_path, filename)
        doc_name = filename.replace(".docx", "")
        extract_paragraphs(doc_path, doc_name)

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(chunks, f, indent=2, ensure_ascii=False)
print(f"Ingested {len(chunks)} content chunks into {output_file}")
