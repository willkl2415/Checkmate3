import json

# Load chunk data once
with open("data/chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

def get_answer(question, selected_document=None, selected_section=None):
    if not question or not question.strip():
        return "Please enter a valid question."

    question = question.strip().lower()
    results = []

    for chunk in chunks:
        content = chunk.get("content", "").lower()
        document = chunk.get("document", "")
        section = chunk.get("section", "")

        # Match content
        if question in content:
            # Apply optional filters
            if selected_document and selected_document != document:
                continue
            if selected_section and selected_section != section:
                continue

            results.append({
                "document": document,
                "section": section,
                "content": chunk["content"]
            })

    if not results:
        return "No relevant answers found. Try a different word or phrase."

    # Format response
    response = ""
    for i, res in enumerate(results[:10], 1):
        response += f"**Result {i}:**\n"
        response += f"**Document:** {res['document']}\n"
        response += f"**Section:** {res['section']}\n"
        response += f"{res['content']}\n\n"

    return response
