import json
import re

with open("data/chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

def get_answer(query, document_filter="", section_filter=""):
    query_lower = query.lower()
    matches = []

    for i, chunk in enumerate(chunks):
        doc = chunk.get("document", "")
        section = chunk.get("section", "")
        heading = chunk.get("heading", "")
        content = chunk.get("content", "")

        if document_filter and doc != document_filter:
            continue
        if section_filter and section != section_filter:
            continue

        combined = f"{heading} {content}".lower()
        if query_lower in combined:
            display_section = f"Section {section} – " if section else ""
            result = (
                f"Document: {doc}\n"
                f"Result {len(matches) + 1}:\n"
                f"Content: {display_section}{heading}\n{content}"
            )
            matches.append(result)

        if len(matches) >= 50:
            return matches, True

    return matches, False
