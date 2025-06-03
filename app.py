# app.py
import os
import json
from flask import Flask, render_template, request
from answer_engine import get_answer

app = Flask(__name__)

# Load document chunks
with open("data/chunks.json", "r", encoding="utf-8") as f:
    chunks_data = json.load(f)

# Load document sections
documents = sorted(set(chunk["document"] for chunk in chunks_data))
document_sections = {}
for chunk in chunks_data:
    doc = chunk["document"]
    section = chunk.get("section", "Uncategorised")
    if doc not in document_sections:
        document_sections[doc] = set()
    document_sections[doc].add(section)

# Convert sets to sorted lists for JSON serialisation
for doc in document_sections:
    document_sections[doc] = sorted(document_sections[doc])

@app.route("/", methods=["GET", "POST"])
def index():
    answer = ""
    question = ""
    results = []
    selected_document = ""
    selected_section = ""
    include_subsections = False

    if request.method == "POST":
        question = request.form["question"]
        selected_document = request.form.get("document_filter", "")
        selected_section = request.form.get("section_filter", "")
        include_subsections = request.form.get("include_subsections") == "on"

        filters = {
            "document": selected_document,
            "section": selected_section,
            "include_subsections": include_subsections
        }

        results = get_answer(question, filters=filters)
        answer = results[0]["answer"] if results else "No answer found."

    return render_template(
        "index.html",
        answer=answer,
        question=question,
        results=results,
        documents=documents,
        document_sections=document_sections,
        selected_document=selected_document,
        selected_section=selected_section,
        include_subsections=include_subsections
    )

if __name__ == "__main__":
    app.run(debug=True)
