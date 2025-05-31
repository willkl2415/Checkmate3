# app.py

import os
import json
from flask import Flask, render_template, request
from answer_engine import get_answer

app = Flask(__name__)

# Load the chunk data
with open("data/chunks.json", "r", encoding="utf-8") as f:
    chunks_data = json.load(f)

# Extract document list
documents = sorted(set(chunk["document"] for chunk in chunks_data))

# Create a dictionary of sections per document
document_sections = {}
for chunk in chunks_data:
    doc = chunk["document"]
    section = chunk.get("section", "Uncategorised")
    if doc not in document_sections:
        document_sections[doc] = set()
    document_sections[doc].add(section)

# Convert section sets to sorted lists for UI
for doc in document_sections:
    document_sections[doc] = sorted(document_sections[doc])

@app.route("/", methods=["GET", "POST"])
def index():
    question = ""
    answer = ""
    selected_doc = ""
    selected_section = ""
    filtered_chunks = []

    if request.method == "POST":
        question = request.form.get("question", "")
        selected_doc = request.form.get("document", "")
        selected_section = request.form.get("section", "")

        # Filter chunks based on selection
        filtered_chunks = chunks_data
        if selected_doc:
            filtered_chunks = [c for c in filtered_chunks if c["document"] == selected_doc]
        if selected_section:
            filtered_chunks = [c for c in filtered_chunks if c.get("section") == selected_section]

        # Get answer using filtered data
        answer, result_count, trimmed = get_answer(question, filtered_chunks)

        return render_template(
            "index.html",
            question=question,
            answer=answer,
            documents=documents,
            sections=document_sections.get(selected_doc, []),
            request=request,
            trimmed=trimmed,
            result_count=result_count,
            document_shown=selected_doc
        )

    # Initial GET render
    return render_template(
        "index.html",
        question="",
        answer="",
        documents=documents,
        sections=[],
        request=request,
        trimmed=False,
        result_count=0,
        document_shown=""
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
