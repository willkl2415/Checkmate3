import json

# Load the document chunks from chunks.json
with open("chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

def get_answer(query, selected_document=None, selected_section=None):
    """
    Searches for the query across all chunks, optionally filtered by document and section.

    Args:
        query (str): The user input query or keyword.
        selected_document (str): Optional filter by document name.
        selected_section (str): Optional filter by section name.

    Returns:
        list of dict: List of matched chunks containing document, section, and content.
    """
    query_lower = query.lower()
    results = []

    for chunk in chunks:
        doc = chunk.get("document", "")
        section = chunk.get("section", "")
        content = chunk.get("content", "")

        if selected_document and doc != selected_document:
            continue
        if selected_section and section != selected_section:
            continue

        # Match if query appears in the section or the content
        if query_lower in section.lower() or query_lower in content.lower():
            results.append({
                "document": doc,
                "section": section,
                "content": content
            })

    return results
