import docx
import os
import json

DOCS_FOLDER = "docs"
chunks = []

def extract_docx_text(doc_path):
    doc = docx.Document(doc_path)
    text_blocks = []
    current_section = "Unknown"
    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue
        if para.style.name.startswith("Heading"):
            current_section = text
        else:
            text_blocks.append((current_section, text))
    return text_blocks

for filename in os.listdir(DOCS_FOLDER):
    if filename.endswith(".docx") and not filename.startswith("~$"):
        path = os.path.join(DOCS_FOLDER, filename)
        print(f"Processing {filename}")
        text_blocks = extract_docx_text(path)
        for section, content in text_blocks:
            chunks.append({
                "source": filename,
                "section": section,
                "content": content
            })

with open("data/chunks.json", "w", encoding="utf-8") as f:
    json.dump(chunks, f, ensure_ascii=False, indent=2)

print("Ingestion complete.")

