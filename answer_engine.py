# answer_engine.py
import json
import tiktoken
from preprocess_pipeline import clean_text

with open("data/chunks.json", "r", encoding="utf-8") as f:
    chunks_data = json.load(f)

encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")

def num_tokens_from_string(string: str) -> int:
    return len(encoding.encode(string))

def get_answer(query, filters=None):
    if not query:
        return []

    query = query.lower().strip()
    filtered_chunks = []

    selected_doc = filters.get("document") if filters else None

    for chunk in chunks_data:
        doc_match = (
            selected_doc in [None, "", "All Documents"] or
            chunk["document"] == selected_doc
        )

        if not doc_match:
            continue

        text = clean_text(chunk["content"])
        if query in text.lower():
            filtered_chunks.append(chunk)

    return filtered_chunks
