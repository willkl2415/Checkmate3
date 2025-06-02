# answer_engine.py

import json
import re
import tiktoken
import openai

# Load chunks once at startup
with open("data/chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

# Helper to count tokens (ensures we don’t exceed context window)
def count_tokens(text):
    encoding = tiktoken.encoding_for_model("gpt-4")
    return len(encoding.encode(text))

# Helper to clean and format answers
def format_result(result):
    return {
        "document": result["document"],
        "section": result.get("section", "Uncategorised"),
        "content": result["content"]
    }

# Section inclusion logic
def matches_section_filter(chunk_section, selected_section, include_subsections):
    if not chunk_section or not selected_section:
        return False
    if include_subsections:
        return chunk_section.startswith(selected_section)
    return chunk_section == selected_section

# Filter logic
def filter_chunks(chunks, filters):
    if not filters:
        return chunks

    filtered = []
    selected_doc = filters.get("document", "")
    selected_section = filters.get("section", "")
    include_subs = filters.get("include_subsections", False)

    for chunk in chunks:
        if selected_doc and chunk["document"] != selected_doc:
            continue
        if selected_section:
            chunk_section = chunk.get("section", "Uncategorised")
            if not matches_section_filter(chunk_section, selected_section, include_subs):
                continue
        filtered.append(chunk)
    return filtered

# Search algorithm
def search_chunks(question, filters=None, max_results=30):
    question_lower = question.lower()
    filtered_chunks = filter_chunks(chunks, filters)
    matches = []

    for chunk in filtered_chunks:
        text = chunk["content"].lower()
        if question_lower in text or any(word in text for word in question_lower.split()):
            matches.append(chunk)
        if len(matches) >= max_results:
            break

    return [format_result(m) for m in matches]

# Main function called by app.py
def get_answer(question, filters=None):
    if not question:
        return []

    results = search_chunks(question, filters=filters)
    return results
