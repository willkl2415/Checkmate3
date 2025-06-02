# app.py
import os
import json
from flask import Flask, render_template, request
from answer_engine import get_answer

app = Flask(__name__)

# Load and process chunks.json
with open("data/chunks.json", "r", encoding="utf-8") as f:
    chunks_data = json.load(f)

# Extract document list
documents = sorted(set(chunk["document"] for chunk in chunks_data))

# Build document_sections dictionary
document_sections = {}
for chunk in chunks_data:
    doc = chunk.get("document")
    section = chunk.get("section", "").strip()
    if doc and section:
        document_sections.setdefault(doc, set()).add(section)

# Convert sets to sorted lists for JSON serialization
for doc in document_sections:
    document_sections[doc] = sorted(document_sections[doc])

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    question = ""
    selected_doc = ""
    selected_section = ""
    include_subsections = False

    if request.method == "POST":
        question = request.form.get("question", "")
        selected_doc = request.form.get("document", "")
        selected_section = request.form.get("section", "")
        include_subsections = bool(request.form.get("include_subsections"))

        filters = {}
        if selected_doc and selected_doc != "All Documents":
            filters["document"] = selected_doc
        if selected_section and selected_section != "All Sections":
            filters["section"] = selected_section
            if include_subsections:
                filters["include_subsections"] = True

        results = get_answer(question, filters=filters)

    return render_template(
        "index.html",
        results=results,
        question=question,
        documents=["All Documents"] + documents,
        selected_doc=selected_doc,
        selected_section=selected_section,
        document_sections=document_sections,
        include_subsections=include_subsections
    )

if __name__ == "__main__":
    app.run(debug=True)
