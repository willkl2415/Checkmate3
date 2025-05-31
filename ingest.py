import os
import json
from docx import Document

def extract_chunks_from_docx(file_path, document_name):
    doc = Document(file_path)
    chunks = []
    current_heading = ""
    current_section = ""
    buffer = []

    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue
        if para.style.name.startswith("Heading"):
            if buffer:
                chunks.append({
                    "document": document_name,
                    "heading": current_heading,
                    "section": current_section,
                    "content": " ".join(buffer).strip()
                })
                buffer = []
            current_heading = text
            match = re.match(r"^(\d+(\.\d+)*)(\s+.*)?", text)
            current_section = match.group(1) if match else ""
        else:
            buffer.append(text)

    if buffer:
        chunks.append({
            "document": document_name,
            "heading": current_heading,
            "section": current_section,
            "content": " ".join(buffer).strip()
        })

    return chunks

if __name__ == "__main__":
    docs_folder = "docs"
    output_path = "data/chunks.json"
    all_chunks = []

    for filename in os.listdir(docs_folder):
        if filename.endswith(".docx"):
            path = os.path.join(docs_folder, filename)
            chunks = extract_chunks_from_docx(path, filename)
            all_chunks.extend(chunks)

    os.makedirs("data", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2, ensure_ascii=False)

    print(f"Ingested {len(all_chunks)} chunks.")
