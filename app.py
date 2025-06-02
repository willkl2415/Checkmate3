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
    section = chunk.get("section")
    if section and section.strip():
        if doc not in document_sections:
            document_sections[doc] = set()
        document_sections[doc].add(section)

for doc in document_sections:
    document_sections[doc] = sorted(document_sections[doc])

@app.route("/", methods=["GET", "POST"])
def index():
    answer = ""
    question = ""
    selected_doc = ""
    selected_section = ""
    filtered_sections = []
    include_subsections = False

    if request.method == "POST":
        question = request.form["question"]
        selected_doc = request.form["document"]
        selected_section = request.form["section"]
        include_subsections = "include_subsections" in request.form
        answer = get_answer(question, selected_doc, selected_section, include_subsections)

    if selected_doc in document_sections:
        filtered_sections = document_sections[selected_doc]

    return render_template(
        "index.html",
        answer=answer,
        question=question,
        documents=documents,
        selected_doc=selected_doc,
        sections=filtered_sections,
        selected_section=selected_section,
        include_subsections=include_subsections,
    )

if __name__ == "__main__":
    app.run(debug=True)
