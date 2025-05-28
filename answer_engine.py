import json
import os

def load_chunks():
    file_path = os.path.join("data", "chunks.json")
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def answer_question(query):
    chunks = load_chunks()
    query_lower = query.lower()

    results = []
    for chunk in chunks:
        text = chunk["content"].lower()
        if query_lower in text:
            results.append({
                "document": chunk.get("document", "Unknown"),
                "heading": chunk.get("heading", "Unknown"),
                "content": chunk.get("content", "")
            })

    return results
