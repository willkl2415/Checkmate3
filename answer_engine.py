# answer_engine.py

import json
import re
from difflib import SequenceMatcher

with open("data/chunks.json", "r", encoding="utf-8") as f:
    chunks_data = json.load(f)

def clean_text(text):
    # Basic cleaner to normalise whitespace
    return re.sub(r"\s+", " ", text.strip().lower())

def matches_filter(chunk, filters):
    if not filters:
        return True

    doc_match = True
    sec_match = True

    if "document" in filters and filters["document"]:
        doc_match = chunk["document"] == filters["document"]

    if "section" in filters and filters["section"]:
        # Standard or subsection match
        if filters.get("include_subsections"):
            sec_match = chunk["section"].startswith(filters["section"])
        else:
            sec_match = chunk["section"] == filters["section"]

    return doc_match and sec_match

def get_answer(question, filters=None):
    if not question.strip():
        return []

    cleaned_question = clean_text(question)
    matches = []

    for chunk in chunks_data:
        if not matches_filter(chunk, filters):
            continue

        chunk_text = clean_text(chunk["text"])
        similarity = SequenceMatcher(None, cleaned_question, chunk_text).ratio()

        if (
            cleaned_question in chunk_text
            or chunk_text in cleaned_question
            or similarity > 0.45
        ):
            matches.append({
                "document": chunk.get("document", "Unknown Document"),
                "section": chunk.get("section", "Uncategorised"),
                "text": chunk.get("text", ""),
            })

    return matches
