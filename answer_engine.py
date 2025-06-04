# answer_engine.py
import json
import tiktoken
from preprocess_pipeline import clean_text

with open("data/chunks.json", "r", encoding="utf-8") as f:
    chunks_data = json.load(f)

encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")

def num_tokens_from_string(string: str) -> int:
    return len(encoding.encode(string))

def get_answer(question, filters=None):
    if not question:
        return []

    question = question.strip().lower()
    filtered_chunks = []

    selected_doc = filters.get("document") if filters else None
    refine_query = filters.get("refine_query", "").strip().lower() if filters else ""

    for chunk in chunks_data:
        if selected_doc and selected_doc not in ["", "All Documents"] and chunk["document"] != selected_doc:
            continue

        chunk_text = clean_text(chunk["content"])
        if question in chunk_text.lower() or refine_query in chunk_text.lower():
            filtered_chunks.append(chunk)

    return filtered_chunks
