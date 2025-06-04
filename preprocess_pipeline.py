import os
import json
import uuid
import re
import docx
from docx.text.paragraph import Paragraph

# === CONFIGURATION ===
INPUT_FILE = "docs/DTSM 2 Analysis of Individual Training 2023 Edition V1.0.docx"
OUTPUT_FILE = "data/chunks.json"
DOCUMENT_NAME = "DTSM 2 Analysis of Individual Training 2023 Edition V1.0"
MAX_PARAGRAPHS_PER_CHUNK = 3

# === OFFICIAL TOC MAP (provided manually) ===
TOC_MAP = {
    "1": "How to use this Manual",
    "2": "Introduction to Analysis of Training",
    "2.1": "Training Needs Analysis",
    "3": "TNA Governance",
    "3.1": "Introduction",
    "3.2": "Training Support Plan",
    "4": "Scoping Exercise",
    "4.1": "Introduction",
    "4.3": "TNA Terms of References",
    "4.3a": "TNA Plan",
    "4.4": "Training Audience (and Throughput) Description",
    "4.5": "Constraints Analysis",
    "4.6": "The Scoping Exercise Report",
    "5": "Role Analysis",
    "5.1": "Introduction",
    "5.2": "Identification of Role",
    "5.3": "Production of Role Scalar",
    "5.4": "DIF Analysis",
    "5.5": "Knowledge, Skills and Attitude Analysis",
    "5.6": "Initial Training Categorisation",
    "5.7": "Role Performance Statement",
    "5.8": "Frameworks",
    "5.9": "Recommended Further Reading",
    "6": "Training Gap Analysis",
    "6.1": "Introduction",
    "6.2": "Statement of Training Gaps",
    "7": "Training Objectives",
    "8": "Training Options Analysis",
    "8.1": "Introduction",
    "8.2": "Fidelity Analysis",
    "8.3": "Location / Environment Implications",
    "8.4": "Methods and Media Options",
    "8.5": "Cost Benefit Analysis",
    "8.6": "Options Evaluation",
    "8.7": "Recommended Further Reading",
    "9": "Training Needs Report",
    "10": "Annexes",
    "A": "Initial KSA Analysis (KSA) Example",
    "B": "Role Performance Statement (Role PS) Example",
    "C": "Fidelity Analysis Example",
    "11": "Document Information",
    "11.1": "Document Coverage",
    "11.2": "Document Information",
    "11.3": "Document Editions / Versions"
}

# === REGEX TO MATCH SECTION HEADINGS ===
SECTION_PATTERN = re.compile(r"^(\d{1,2}(?:\.\d{1,2})?|[A-C])\s{1,3}(.+)$")

def clean_text(text):
    return re.sub(r"\s+", " ", text).strip()

def extract_paragraphs(docx_file):
    doc = docx.Document(docx_file)
    return [clean_text(p.text) for p in doc.paragraphs if p.text.strip()]

def generate_chunks(paragraphs):
    chunks = []
    buffer = []
    current_section = None
    section_count = {}

    for para in paragraphs:
        match = SECTION_PATTERN.match(para)
        if match:
            raw_num = match.group(1)
            title = match.group(2).strip()

            if raw_num in section_count:
                # disambiguate duplicate e.g. 4.3, 4.3a, 4.3b, etc.
                suffix = chr(ord('a') + section_count[raw_num])
                raw_num += suffix
                section_count[raw_num[:-1]] += 1
            else:
                section_count[raw_num] = 1

            section_title = TOC_MAP.get(raw_num, title)
            if buffer:
                chunks.append({
                    "id": str(uuid.uuid4()),
                    "document": DOCUMENT_NAME,
                    "section": current_section if current_section else "Uncategorised",
                    "content": " ".join(buffer)
                })
                buffer = []

            current_section = f"{raw_num} {section_title}"
            continue

        if current_section is None:
            continue

        buffer.append(para)
        if len(buffer) >= MAX_PARAGRAPHS_PER_CHUNK:
            chunks.append({
                "id": str(uuid.uuid4()),
                "document": DOCUMENT_NAME,
                "section": current_section,
                "content": " ".join(buffer)
            })
            buffer = []

    if buffer:
        chunks.append({
            "id": str(uuid.uuid4()),
            "document": DOCUMENT_NAME,
            "section": current_section if current_section else "Uncategorised",
            "content": " ".join(buffer)
        })

    return chunks

def main():
    os.makedirs("data", exist_ok=True)
    paragraphs = extract_paragraphs(INPUT_FILE)
    chunks = generate_chunks(paragraphs)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
