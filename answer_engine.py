# answer_engine.py

import json
import re

def get_answer(question, chunks):
    question_lower = question.lower()
    results = []

    for chunk in chunks:
        content = chunk["content"].lower()
        if question_lower in content or all(word in content for word in question_lower.split()):
            results.append(chunk)

    # Trim to a max of 100 results for display
    trimmed = False
    if len(results) > 100:
        results = results[:100]
        trimmed = True

    # Format result
    answer_text = ""
    for i, res in enumerate(results, 1):
        answer_text += (
            f"Document: {res['document']}\n"
            f"Section: {res.get('section', 'Uncategorised')}\n"
            f"Result {i}:\n"
            f"{res['content']}\n\n"
        )

    if not answer_text:
        answer_text = "No relevant information found in the selected document(s)."

    return answer_text, len(results), trimmed
