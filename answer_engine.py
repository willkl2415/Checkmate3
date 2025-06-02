import json
import os

# Load all chunks into memory once
CHUNKS_PATH = os.path.join("data", "chunks.json")
with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
    chunks_data = json.load(f)

def get_answer(question, selected_document=None, selected_section=None, include_subsections=False):
    """Return list of chunks matching the selected filters and containing relevant content."""
    results = []

    # Normalize selections
    selected_document = selected_document.strip() if selected_document else None
    selected_section = selected_section.strip() if selected_section else None

    for chunk in chunks_data:
        doc_match = not selected_document or chunk["document"] == selected_document
        sec_match = False

        if not selected_section:
            sec_match = True
        elif include_subsections:
            sec_match = chunk.get("section", "").startswith(selected_section)
        else:
            sec_match = chunk.get("section", "") == selected_section

        if doc_match and sec_match and question.lower() in chunk["content"].lower():
            results.append(chunk)

    return results
