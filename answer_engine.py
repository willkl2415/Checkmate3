import json
import os

def answer_question(user_input):
    chunks_path = os.path.join("data", "chunks.json")
    with open(chunks_path, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    results = []
    user_input_lower = user_input.lower()

    for chunk in chunks:
        content = chunk.get("content", "").lower()
        if user_input_lower in content:
            results.append({
                "document": chunk.get("document", "Unknown"),
                "heading": chunk.get("heading", "Unknown"),
                "content": chunk.get("content", "")
            })

    return results
