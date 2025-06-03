# answer_engine.py
import json
import re
import tiktoken

with open("data/chunks.json", "r", encoding="utf-8") as f:
    chunks_data = json.load(f)

def count_tokens(text):
    enc = tiktoken.get_encoding("cl100k_base")
    return len(enc.encode(text))

def get_answer(question, selected_doc, selected_section, include_subsections):
    matches = []

    for chunk in chunks_data:
        if selected_doc != "All Documents" and chunk["document"] != selected_doc:
            continue
        if selected_section != "All Sections":
            chunk_section = chunk.get("section", "Uncategorised")
            if include_subsections:
                if not chunk_section.startswith(selected_section):
                    continue
            else:
                if chunk_section != selected_section:
                    continue
        if question.lower() in chunk["content"].lower():
            matches.append(chunk)

    if not matches:
        return {
            "answer": "Check-Mate’s Response (0 results)",
            "matches": [],
            "message": "Use the document filter to view all matches."
        }

    matches.sort(key=lambda x: x["content"].lower().find(question.lower()))
    context = "\n\n".join([m["content"] for m in matches[:3]])
    references = [{
        "document": m["document"],
        "section": m.get("section", "Uncategorised"),
        "content": m["content"]
    } for m in matches]

    return {
        "answer": f"Check-Mate’s Response ({len(matches)} results)",
        "matches": references,
        "message": "Use the document filter to view all matches."
    }
