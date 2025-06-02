# app.py
import os
import json
import re
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

def section_key(s):
    return [int(part) if part.isdigit() else part for part in re.split(r'(\d+)', s)]

for doc in document_sections:
    document_sections[doc] = sorted(set(document_sections[doc]), key=section_key)

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    question = ""
    selected_doc = "All Documents"
    selected_section = "All Sections"
    include_subsections = False

    if request.method == "POST":
        question = request.form["question"].strip()
        selected_doc = request.form.get("document", "All Documents")
        selected_section = request.form.get("section", "All Sections")
        include_subsections = request.form.get("includeSubsections") == "on"

        filters = {
            "document": selected_doc,
            "section": selected_section,
            "include_subsections": include_subsections
        }

        if question:
            results = get_answer(question, filters=filters)

    return render_template(
        "index.html",
        results=results,
        question=question,
        documents=["All Documents"] + documents,
        selected_doc=selected_doc,
        sections=["All Sections"] + sorted(set(sum(document_sections.values(), [])), key=section_key),
        selected_section=selected_section,
        include_subsections=include_subsections,
        document_sections=document_sections
    )

if __name__ == "__main__":
    app.run(debug=True)
