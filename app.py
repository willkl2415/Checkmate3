# app.py
import os
from flask import Flask, render_template, request
from answer_engine import get_answer
import json

app = Flask(__name__)

with open("data/chunks.json", "r", encoding="utf-8") as f:
    chunks_data = json.load(f)

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
    answer = ""
    question = ""
    selected_doc = "All Documents"
    selected_section = "All Sections"
    include_subsections = False

    if request.method == "POST":
        question = request.form.get("question", "")
        selected_doc = request.form.get("document", "All Documents")
        selected_section = request.form.get("section", "All Sections")
        include_subsections = request.form.get("include_subsections") == "on"

        results = get_answer(question, selected_doc, selected_section, include_subsections)
        answer = results

    return render_template(
        "index.html",
        answer=answer,
        question=question,
        documents=documents,
        document_sections=document_sections,
        selected_doc=selected_doc,
        selected_section=selected_section,
        include_subsections=include_subsections,
    )

if __name__ == "__main__":
    app.run(debug=True)
