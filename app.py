# app.py
import os
import json
from flask import Flask, render_template, request
from answer_engine import get_answer

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
document_sections = {k: sorted(v) for k, v in document_sections.items()}

@app.route("/", methods=["GET", "POST"])
def index():
    answer = ""
    question = ""
    selected_doc = "All Documents"
    selected_section = "All Sections"
    include_subsections = False

    if request.method == "POST":
        question = request.form["question"]
        selected_doc = request.form["document"]
        selected_section = request.form["section"]
        include_subsections = request.form.get("include_subsections") == "on"

        filters = {
            "document": selected_doc,
            "section": selected_section,
            "include_subsections": include_subsections,
        }

        results = get_answer(question, filters=filters)
        answer = results

    return render_template(
        "index.html",
        answer=answer,
        question=question,
        documents=["All Documents"] + documents,
        sections=["All Sections"],
        document_sections=document_sections,
        selected_doc=selected_doc,
        selected_section=selected_section,
        include_subsections=include_subsections
    )

if __name__ == "__main__":
    app.run(debug=True)
