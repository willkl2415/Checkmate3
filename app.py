# app.py
import os
import json
from flask import Flask, render_template, request
from answer_engine import get_answer

app = Flask(__name__)

# Load chunks.json
with open("data/chunks.json", "r", encoding="utf-8") as f:
    chunks_data = json.load(f)

# Build document and section listings
documents = sorted(set(chunk["document"] for chunk in chunks_data))
document_sections = {}
for chunk in chunks_data:
    doc = chunk["document"]
    section = chunk.get("section", "Uncategorised")
    if doc not in document_sections:
        document_sections[doc] = set()
    document_sections[doc].add(section)

@app.route("/", methods=["GET", "POST"])
def index():
    question = ""
    answer = []
    selected_doc = ""
    refine_query = ""

    if request.method == "POST":
        if "clear" in request.form:
            return render_template(
                "index.html",
                question="",
                answer=[],
                documents=documents,
                selected_doc="",
                refine_query="",
                sections={},
            )

        question = request.form.get("question", "").strip()
        selected_doc = request.form.get("document", "")
        refine_query = request.form.get("refine_query", "").strip()

        filtered_chunks = chunks_data

        # Filter by selected document
        if selected_doc:
            filtered_chunks = [c for c in filtered_chunks if c["document"] == selected_doc]

        # Apply refine query filter
        if refine_query:
            filtered_chunks = [c for c in filtered_chunks if refine_query.lower() in c["content"].lower()]

        # Run main query
        if question:
            answer = get_answer(question, filtered_chunks)
        else:
            answer = filtered_chunks

    return render_template(
        "index.html",
        question=question,
        answer=answer,
        documents=documents,
        selected_doc=selected_doc,
        refine_query=refine_query,
        sections=document_sections.get(selected_doc, []),
    )

if __name__ == "__main__":
    app.run(debug=True)
