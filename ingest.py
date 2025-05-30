import docx
import json
import os

def extract_text_from_docx(filepath):
    doc = docx.Document(filepath)
    text_by_heading = {}
    current_heading = "Unknown Section"

    for para in doc.paragraphs:
        style = para.style.name
        text = para.text.strip()

        if style.startswith("Heading") and text:
            current_heading = text
            if current_heading not in text_by_heading:
                text_by_heading[current_heading] = []
        elif text:
            text_by_heading.setdefault(current_heading, []).append(text)

    return text_by_heading

def ingest_documents(folder_path):
    chunks = []
    for filename in os.listdir(folder_path):
        if filename.startswith("~$") or not filename.endswith(".docx"):
            continue
        path = os.path.join(folder_path, filename)
        doc_name = os.path.splitext(filename)[0]
        sections = extract_text_from_docx(path)

        for heading, paras in sections.items():
            content = "\n".join(paras)
            chunks.append({
                "document": doc_name,
                "heading": heading,
                "content": content
            })

    with open("chunks.json", "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    ingest_documents("docs")
