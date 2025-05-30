import json

def get_answer(query, selected_document="", selected_section=""):
    if not query:
        return "Please enter a question."

    with open("chunks.json", "r", encoding="utf-8") as f:
        chunks = json.load(f)

    matches = []
    for chunk in chunks:
        content = chunk["content"].lower()
        heading = chunk["heading"].lower()
        document = chunk["document"]

        if selected_document and chunk["document"] != selected_document:
            continue
        if selected_section and chunk["heading"] != selected_section:
            continue

        if query.lower() in content or query.lower() in heading:
            matches.append(chunk)

    if not matches:
        return "No relevant information found in the selected documents."

    result = ""
    for match in matches:
        result += f"<b>{match['document']} – {match['heading']}</b><br>{match['content']}<br><br>"

    return result
