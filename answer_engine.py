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
    for chunk in chunks_data:
        if filters:
            doc_match = not filters.get("document") or chunk["document"] == filters["document"]
            section_match = not filters.get("section") or chunk.get("section", "") == filters["section"]
            subsection = filters.get("include_subsections", False)
            if not subsection and not section_match:
                continue
            if not (doc_match and section_match):
                continue

        chunk_text = clean_text(chunk["content"])
        if question in chunk_text.lower():
            filtered_chunks.append(chunk)

    return filtered_chunks
