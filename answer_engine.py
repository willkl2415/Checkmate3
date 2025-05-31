import os
import docx

def get_answer(question, selected_document=None, selected_section=None):
    docs_path = "docs"
    question = question.strip().lower()
    results = []

    if not question:
        return "Please enter a valid question."

    for filename in os.listdir(docs_path):
        if filename.endswith(".docx"):
            if selected_document and selected_document != filename:
                continue  # skip if user selected a specific doc

            filepath = os.path.join(docs_path, filename)
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

    if not results:
        return "No relevant answers found. Try using a different word."

    # Format results
    response = ""
    for i, res in enumerate(results[:10], 1):
        response += f"**Result {i}:**\n"
        response += f"**Document:** {res['document']}\n"
        response += f"**Content:** {res['content']}\n\n"

    return response
