import os
import json
import uuid
import re
import docx

# === CONFIGURATION ===
INPUT_DIR = "docs"
OUTPUT_FILE = "data/chunks.json"
MAX_PARAGRAPHS_PER_CHUNK = 3
SECTION_PATTERN = re.compile(r"^(\d{1,2}(?:\.\d{1,2})*)\s+(.+)$")

# === CLEANING UTILITY ===
def clean_text(text: str) -> str:
    text = re.sub(r"\[\d+\]", "", text)  # Remove footnote markers like [1]
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# === LOAD PARAGRAPHS FROM DOCX ===
def load_cleaned_paragraphs(file_path):
    doc = docx.Document(file_path)
    paragraphs = [clean_text(p.text) for p in doc.paragraphs if p.text.strip()]
    return paragraphs

# === CHUNKING LOGIC ===
def generate_chunks(paragraphs, document_name):
    chunks = []
    current_section = None
    buffer = []
    section_started = False

    for para in paragraphs:
        match = SECTION_PATTERN.match(para)
        if match:
            if buffer:
                chunks.append({
                    "id": str(uuid.uuid4()),
                    "document": document_name,
                    "section": current_section or "Uncategorised",
                    "content": " ".join(buffer)
                })
                buffer = []
            current_section = f"{match.group(1)} {match.group(2)}"
            section_started = True
            continue

        if not section_started:
            continue

        buffer.append(para)
        if len(buffer) >= MAX_PARAGRAPHS_PER_CHUNK:
            chunks.append({
                "id": str(uuid.uuid4()),
                "document": document_name,
                "section": current_section or "Uncategorised",
                "content": " ".join(buffer)
            })
            buffer = []

    if buffer:
        chunks.append({
            "id": str(uuid.uuid4()),
            "document": document_name,
            "section": current_section or "Uncategorised",
            "content": " ".join(buffer)
        })

    return chunks

# === MAIN EXECUTION ===
def main():
    os.makedirs("data", exist_ok=True)
    all_chunks = []

    files = os.listdir(INPUT_DIR)
    print(f"[INFO] Files in /docs: {files}")

    for file_name in files:
        if file_name.endswith(".docx"):
            file_path = os.path.join(INPUT_DIR, file_name)
            try:
                print(f"[INFO] Processing: {file_name}")
                paragraphs = load_cleaned_paragraphs(file_path)
                doc_name = file_name.replace(".docx", "")
                chunks = generate_chunks(paragraphs, doc_name)
                all_chunks.extend(chunks)
                print(f"[SUCCESS] {file_name} => {len(chunks)} chunks")
            except Exception as e:
                print(f"[ERROR] Failed to process {file_name}: {e}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2, ensure_ascii=False)

    print(f"[DONE] Total chunks written: {len(all_chunks)}")

if __name__ == "__main__":
    main()
