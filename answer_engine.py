import json

def get_answer(question, selected_document=None, selected_section=None):
    with open("data/chunks.json", "r", encoding="utf-8") as f:
        chunks_data = json.load(f)

    question = question.strip().lower()
    if not question:
        return "Please enter a valid question.", 0, False, ""

    results = []
    debug_log = []
    scanned_docs = set()

    for chunk in chunks_data:
        document = chunk.get("document", "")
        heading = chunk.get("heading", "")
        content = chunk.get("content", "")

        # Apply optional filters
        if selected_document and selected_document != document:
            continue
        if selected_section and selected_section != heading:
            continue

        # Scan for question match
        if question in content.lower() or question in heading.lower():
            results.append((document, heading, content))
            scanned_docs.add(document)

    total_results = len(results)
    trimmed = False
    trim_limit = 25

    if not results:
        return "No results found.", 0, False, ""

    response = ""
    if not selected_document:
        for doc in sorted(scanned_docs):
            response += f"Scanning file: {doc}\n"
    else:
        response += f"Scanning file: {selected_document}\n"

    if selected_section:
        response += f"Scanning section: {selected_section}\n"

    response += "\n"

    for idx, (document, heading, content) in enumerate(results[:trim_limit], 1):
        response += f"Document: {document}\n"
        response += f"Section: {heading}\n"
        response += f"Result {idx}:\nContent: {content}\n\n"

    if total_results > trim_limit:
        trimmed = True

    return response.strip(), total_results, trimmed, selected_document or ""
