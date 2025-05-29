import json

with open("chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)


def answer_question(question, selected_doc="", selected_section=""):
    if not question.strip():
        return "Please enter a valid question."

    results = []
    for chunk in chunks:
        if selected_doc and chunk["source"] != selected_doc:
            continue
        if selected_section and chunk.get("section", "") != selected_section:
            continue
        if question.lower() in chunk["content"].lower():
            results.append(chunk)

    if not results:
        return "No matching results found in the documents."

    formatted = ""
    for r in results:
        formatted += f"<strong>{r['source']} | {r.get('section', 'Unknown')}</strong><br>{r['content']}<br><br>"
    return formatted
