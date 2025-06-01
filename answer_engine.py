# answer_engine.py
import re
import json

# Load the ToC-enhanced chunks.json
with open("data/chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

def get_answer(question, document_filter=None, section_filter=None):
    question = question.lower()
    keywords = set(re.findall(r"\b\w+\b", question))

    matched_chunks = []

    for chunk in chunks:
        # Filter by document
        if document_filter and chunk["document"] != document_filter:
            continue

        # Filter by ToC section if available
        if section_filter and chunk.get("toc_section") != section_filter:
            continue

        # Basic keyword matching
        content = chunk["content"].lower()
        score = sum(1 for word in keywords if word in content)

        if score > 0:
            matched_chunks.append({
                "document": chunk["document"],
                "section": chunk.get("toc_section", chunk.get("section", "Uncategorised")),
                "content": chunk["content"],
                "score": score
            })

    # Sort results by keyword relevance
    matched_chunks.sort(key=lambda x: x["score"], reverse=True)
    return matched_chunks
