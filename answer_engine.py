import json
import re

def load_chunks():
    with open("data/chunks.json", "r", encoding="utf-8") as file:
        return json.load(file)

def answer_question(query):
    query = query.lower()
    chunks = load_chunks()
    matched_chunks = []

    for chunk in chunks:
        content = chunk["content"].lower()
        if all(term in content for term in query.split()):
            matched_chunks.append(chunk)

    if not matched_chunks:
        return "No matching results found in the documents."

    result = ""
    for chunk in matched_chunks:
        section = chunk["section"]
        content = chunk["content"].strip()
        doc = chunk["document"]
        result += f"<strong>{doc} | {section}</strong><br>{content}<br><br>"

    return result
