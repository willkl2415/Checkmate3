import json

def load_chunks():
    with open("chunks.json", "r", encoding="utf-8") as f:
        return json.load(f)

def answer_question(query):
    query = query.lower()
    for chunk in load_chunks():
        if all(word in chunk["content"].lower() for word in query.split()):
            return f"{chunk['document']} | {chunk['heading']}\n\n{chunk['content']}"
    return "No relevant content found for your question in the loaded documents."