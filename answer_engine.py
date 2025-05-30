import json

with open("chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

def answer_question(query, selected_doc=None, selected_section=None):
    results = []
    query_lower = query.lower()

    for chunk in chunks:
        if selected_doc and chunk["document"] != selected_doc:
            continue
        if selected_section and chunk["heading"] != selected_section:
            continue
        if query_lower in chunk["content"].lower():
            results.append(chunk)

    return results
