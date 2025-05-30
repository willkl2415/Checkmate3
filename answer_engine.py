import json

with open("data/chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

def answer_question(query, selected_doc=""):
    matches = []
    query_lower = query.lower()

    for chunk in chunks:
        content_lower = chunk["content"].lower()
        if query_lower in content_lower:
            if selected_doc == "" or chunk["document"] == selected_doc:
                matches.append(chunk)

    if matches:
        response = ""
        for match in matches:
            response += f"<strong>{match['document']} | {match['heading']}</strong><br>{match['content']}<br><br>"
        return response.strip()
    else:
        return f"<strong>{selected_doc or 'All Documents'} | No Match Found</strong><br>No results found in {selected_doc or 'any document'} for your query."
