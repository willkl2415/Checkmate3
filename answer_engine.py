import json
import re

def get_answer(query, selected_document=None, selected_section=None):
    try:
        with open("chunks.json", "r", encoding="utf-8") as f:
            chunks = json.load(f)
    except Exception as e:
        return [f"Error loading chunks.json: {str(e)}"]

    # Normalise query
    query = query.strip().lower()
    query_words = re.findall(r'\w+', query)

    results = []
    for chunk in chunks:
        # Optional document filter
        if selected_document and chunk.get("document") != selected_document:
            continue
        # Optional section filter
        if selected_section and chunk.get("heading") != selected_section:
            continue

        heading = chunk.get("heading", "").lower()
        content = chunk.get("content", "").lower()

        # Match if any query word appears in heading or content
        if any(word in heading or word in content for word in query_words):
            result = {
                "document": chunk.get("document", "Unknown"),
                "heading": chunk.get("heading", "Unknown"),
                "content": chunk.get("content", "No content available.")
            }
            results.append(result)

    if not results:
        return ["No relevant information found in the selected documents."]

    # Format the results into readable blocks
    formatted = []
    for res in results:
        block = f"**{res['document']} – {res['heading']}**\n{res['content']}"
        formatted.append(block)

    return formatted
