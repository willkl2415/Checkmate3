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
    total_displayed = 0
    trim_limit = 25
    trim_triggered = False

    for filename, matches in grouped_results.items():
        response += f"Document: {filename}\n"
        for i, content in enumerate(matches, 1):
            if not selected_document and total_displayed >= trim_limit:
                trim_triggered = True
                break
            response += f"Result {i}:\nContent: {content}\n\n"
            total_displayed += 1

    if trim_triggered:
        response += "Results trimmed. Use the document filter to view all matches.\n"

    return response
