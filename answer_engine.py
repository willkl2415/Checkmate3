import json
import re

def load_chunks():
    with open("chunks.json", "r", encoding="utf-8") as f:
        return json.load(f)

def clean_text(text):
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def get_answer(question, chunks, selected_doc=None, selected_heading=None):
    question_lower = question.lower()
    results = []

    for chunk in chunks:
        doc_match = selected_doc is None or chunk['document'] == selected_doc
        heading_match = selected_heading is None or chunk['heading'] == selected_heading
        text_match = question_lower in chunk['content'].lower()

        if doc_match and heading_match and text_match:
            results.append({
                'document': chunk['document'],
                'heading': chunk['heading'],
                'content': clean_text(chunk['content'])
            })

    return results
