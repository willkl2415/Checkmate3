import json
import tiktoken
from preprocess_pipeline import clean_text

# Load chunks from file
with open("data/chunks.json", "r", encoding="utf-8") as f:
    chunks_data = json.load(f)

# Token encoding setup
encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")

def num_tokens_from_string(string: str) -> int:
    return len(encoding.encode(string))

def get_answer(question, filters=None):
    if not question:
        return []

    question = question.strip().lower()
    filtered_chunks = []

    selected_doc = filters.get("document") if filters else None
    selected_section = filters.get("section") if filters else None
    include_subsections = filters.get("include_subsections", False) if filters else False

    for chunk in chunks_data:
        # === Document Match ===
        doc_match = selected_doc in [None, "", "All Documents"] or chunk["document"] == selected_doc

        # === Section Match Logic ===
        chunk_section = chunk.get("section", "")
        if selected_section in [None, "", "All Sections"]:
            section_match = True
        elif include_subsections:
            section_match = (
                chunk_section == selected_section or
                chunk_section.startswith(selected_section + ".")
            )
        else:
            section_match = chunk_section == selected_section

        if not (doc_match and section_match):
            continue

        chunk_text = clean_text(chunk["content"])
        if question in chunk_text.lower():
            filtered_chunks.append(chunk)

    return filtered_chunks
