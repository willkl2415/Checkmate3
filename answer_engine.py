# answer_engine.py
import json
import tiktoken
from preprocess_pipeline import clean_text

with open("data/chunks.json", "r", encoding="utf-8") as f:
    chunks_data = json.load(f)

encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")

def num_tokens_from_string(string: str) -> int:
    return len(encoding.encode(string))

def get_answer(question, filters=None, subquery=""):
    if not question:
        return []

    question = question.strip().lower()
    subquery = subquery.strip().lower()
    filtered_chunks = []

    selected_doc = filters.get("document") if filters else None

    for chunk in chunks_data:
        doc_match = selected_doc in [None, "", "All Documents"] or chunk["document"] == selected_doc
        if not doc_match:
            continue

        chunk_text = clean_text(chunk["content"])
        if question in chunk_text.lower():
            filtered_chunks.append(chunk)

    if subquery:
        refined_chunks = []
        for chunk in filtered_chunks:
            if subquery in clean_text(chunk["content"]).lower():
                refined_chunks.append(chunk)
        return refined_chunks

    return filtered_chunks
