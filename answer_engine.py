
def get_priority(doc_title):
    title = doc_title.lower()
    if "jsp 822" in title:
        return 1
    elif "dtsm" in title:
        return 2
    elif "jsp" in title:
        return 3
    elif "mod" in title or "defence" in title:
        return 4
    else:
        return 5

# answer_engine.py
import json
import tiktoken
from preprocess_pipeline import clean_text

# Load chunks
with open("data/chunks.json", "r", encoding="utf-8") as f:
    chunks_data = json.load(f)

encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")

def num_tokens_from_string(string: str) -> int:
    return len(encoding.encode(string))

def get_answer(question, chunks_subset):
    if not question:
        return []

    question = question.strip().lower()
    results = []

    for chunk in chunks_subset:
        chunk_text = clean_text(chunk["content"])
        if question in chunk_text.lower():
            results.append(chunk)

    return results
