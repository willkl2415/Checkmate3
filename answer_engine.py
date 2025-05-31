import os
import docx
from collections import defaultdict

def get_answer(question, selected_document=None, selected_section=None):
    docs_path = "docs"
    question = question.strip().lower()
    grouped_results = defaultdict(list)
    debug_log = []

    if not question:
        return "Please enter a valid question.", 0, False, ""

    for filename in os.listdir(docs_path):
        if filename.endswith(".docx"):
            if selected_document and selected_document != filename:
                continue

            filepath = os.path.join(docs_path, filename)
            debug_log.append(f"Scanning file: {filename}")

            try:
                doc = docx.Document(filepath)
                for para in doc.paragraphs:
                    text = para.text.strip()
                    if not text:
                        continue
                    if question in text.lower():
                        grouped_results[filename].append(text)
            except Exception as e:
                grouped_results[filename].append(f"[ERROR] Could not read file: {e}")

    total_results = sum(len(v) for v in grouped_results.values())
    trimmed = False
    trim_limit = 25

    if not grouped_results:
        return "\n".join(debug_log + ["No results found."]), 0, False, ""

    response = "\n".join(debug_log) + "\n\n"
    shown = 0
    document_label = ""

    for filename, matches in grouped_results.items():
        response += f"Document: {filename}\n"
        document_label = filename if selected_document else ""
        for i, content in enumerate(matches, 1):
            if not selected_document and shown >= trim_limit:
                trimmed = True
                break
            response += f"Result {i}:\nContent: {content}\n\n"
            shown += 1

    return response, total_results, trimmed, document_label
