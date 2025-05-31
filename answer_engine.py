# answer_engine.py
import json
import re

with open("data/chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

def get_answer(question, document_filter=None, section_filter=None):
    question = question.strip().lower()
    matched_chunks = []

    for chunk in chunks:
        if document_filter and chunk["document"] != document_filter:
            continue
        if section_filter and chunk.get("section") != section_filter:
            continue
        if question in chunk["content"].lower() or any(q in chunk["content"].lower() for q in question.split()):
            matched_chunks.append(chunk)

    if not matched_chunks:
        return "No relevant content found for that query."

    result = ""
    for chunk in matched_chunks:
        result += f"<b>{chunk.get('section', 'Uncategorised')}</b><br>{chunk['content']}<br><br>"

    return result
