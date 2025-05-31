import os
import docx

def get_answer(question, selected_document=None, selected_section=None):
    docs_path = "docs"
    question = question.strip().lower()
    results = []
    debug_log = []

    if not question:
        return "Please enter a valid question."

    # Look through every .docx file in the docs folder
    for filename in os.listdir(docs_path):
        if filename.endswith(".docx"):
            if selected_document and selected_document != filename:
                continue

            filepath = os.path.join(docs_path, filename)
            debug_log.append(f"Searching in: {filename}")

            try:
                doc = docx.Document(filepath)
                for para in doc.paragraphs:
                    text = para.text.strip()
                    if not text:
                        continue
                    if question in text.lower():
                        results.append({
                            "document": filename,
                            "section": "N/A",
                            "content": text
                        })
            except Exception as e:
                results.append({
                    "document": filename,
                    "section": "ERROR",
                    "content": f"Could not read file: {e}"
                })

    # Combine debug log and results
    if not results:
        debug_log.append("No matches found for your question.")
        return "\n".join(debug_log)

    response = "\n".join(debug_log) + "\n\n"
    for i, res in enumerate(results[:10], 1):
        response += f"Result {i}:\n"
        response += f"Document: {res['document']}\n"
        response += f"Content: {res['content']}\n\n"

    return response
