import json
import re
import tiktoken
from preprocess_pipeline import clean_text

with open("data/chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

def count_tokens(text):
    encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))

def get_answer(question, filters):
    document_filter = filters.get("document", "")
    section_filter = filters.get("section", "")
    include_subsections = filters.get("include_subsections", False)

    matching_chunks = []
    for chunk in chunks:
        if document_filter and chunk.get("document") != document_filter:
            continue

        chunk_section = str(chunk.get("section", ""))
        if section_filter:
            if include_subsections:
                if not chunk_section.startswith(section_filter):
                    continue
            else:
                if chunk_section != section_filter:
                    continue

        chunk_text = clean_text(chunk["text"])
        if question.lower() in chunk_text.lower():
            matching_chunks.append({
                "document": chunk.get("document", ""),
                "section": chunk.get("section", "Uncategorised"),
                "text": chunk_text
            })

    formatted_results = []
    for i, match in enumerate(matching_chunks, 1):
        formatted_results.append(f"""
<b>Document:</b> {match['document']}<br>
<b>Section:</b> {match['section']}<br>
<b>Result {i}:</b><br>
{match['text'].strip()}<br>
<hr>
""")

    result_html = f"<p><b>Check-Mate’s Response ({len(formatted_results)} results)</b></p>"
    if len(formatted_results) == 0:
        result_html += "<p>Use the document filter to view all matches.</p>"
    result_html += "".join(formatted_results)
    return result_html
