# ingest.py
import os
import json
from docx import Document

SOURCE_FOLDER = "docs"
OUTPUT_FILE = "data/chunks.json"

def extract_section(paragraph, section_headers):
    text = paragraph.text.strip()
    for header in section_headers:
        if text.startswith(header):
            return header
    return None

def parse_document(path, doc_name, section_headers):
    doc = Document(path)
    current_section = "Uncategorised"
    chunks = []

    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue
        new_section = extract_section(para, section_headers)
        if new_section:
            current_section = new_section
        chunks.append({
            "document": doc_name,
            "section": current_section,
            "content": text
        })

    return chunks

def main():
    all_chunks = []
    section_structure = {
        "JSP 822 V7.0 Vol 2 V3.0 Defence Individual Training.docx": [
            "1 Preface", "2 Introduction to Individual Training", "3 Management of Training System",
            "4 Analysis of Individual Training", "5 Designing Individual Training",
            "6 Delivery of Individual Training", "7 Evaluation of Individual Training (Assurance)",
            "8 Defence Trainer Capability", "9 Defence Direction on Remedial Training in Initial Training",
            "10 Defence Direction on Robust Training", "11 Document Information", "12 Applicability", "13 Diversity and Inclusion"
        ],
        "DTSM 2 Analysis of Individual Training 2023 Edition V1.0.docx": [
            "1 How to use this Manual", "2 Introduction to Analysis of Training", "3 TNA Governance",
            "4 Scoping Exercise", "5 Role Analysis", "6 Training Gap Analysis",
            "7 Training Objectives", "8 Training Options Analysis", "9 Training Needs Report",
            "10 Annexes", "11 Document Information"
        ]
    }

    for filename in os.listdir(SOURCE_FOLDER):
        if filename.startswith("~$") or not filename.endswith(".docx"):
            continue
        path = os.path.join(SOURCE_FOLDER, filename)
        headers = section_structure.get(filename, [])
        all_chunks.extend(parse_document(path, filename, headers))

    os.makedirs("data", exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
