import json

def answer_question(query):
    with open('chunks.json', 'r', encoding='utf-8') as f:
        chunks = json.load(f)

    query_lower = query.lower()
    results = []
    for chunk in chunks:
        if query_lower in chunk['content'].lower():
            results.append(chunk)
    return results
