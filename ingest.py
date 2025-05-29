import os
import docx
import json

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    paragraphs = [para.text.strip() for para in doc.paragraphs if para.text.strip()]
    return paragraphs

def get_section_heading(paragraph, last_heading):
    if paragraph.lower().startswith("section"):
        return paragraph
    return last_heading

def process_documents(doc_folder):
    chunks = []
    for filename in os.listdir(doc_folder):
        if filename.endswith(".docx"):
            path = os.path.join(doc_folder, filename)
            paras = extract_text_from_docx(path)
            last_heading = "Unknown"
            for para in paras:
                last_heading = get_section_heading(para, last_heading)
                chunks.append({
                    "document": filename.replace(".docx", ""),
                    "section": last_heading,
                    "content": para
                })
    with open("chunks.json", "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    process_documents("docs")
