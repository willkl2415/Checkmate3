# answer_engine.py
import json
import os

# Load the document chunks from the JSON file
with open("data/chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

def get_answer(query, selected_doc="", selected_section=""):
    results = []
    query_lower = query.lower()

    for chunk in chunks:
        document = chunk.get("document", "")
        heading = chunk.get("heading", "")
        content = chunk.get("content", "")

        # Filter by selected document (if any)
        if selected_doc and document != selected_doc:
            continue

        # Filter by selected section (if any)
        if selected_section and heading != selected_section:
            continue

        # Match query in content or heading (case-insensitive)
        if query_lower in content.lower() or query_lower in heading.lower():
            results.append({
                "document": document,
                "section": heading,
                "content": content.strip()
            })

    return results
