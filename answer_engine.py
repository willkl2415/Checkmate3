import os
import docx
from collections import defaultdict

def get_answer(question, selected_document=None, selected_section=None):
    docs_path = "docs"
    question = question.strip().lower()
    grouped_results = defaultdict(list)
    debug_log = []

    if not question:
        return "Please enter a valid question."

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

    # Format response
    if not grouped_results:
        return "\n".join(debug_log + ["No results found."])

    response = "\n".join(debug_log) + "\n\n"

    for filename, matches in grouped_results.items():
        response += f"Document: {filename}\n"
        for i, content in enumerate(matches, 1):
            response += f"Result {i}:\nContent: {content}\n\n"

    return response
