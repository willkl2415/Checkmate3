import os
import json
import logging
from flask import Flask, render_template, request
from answer_engine import get_answer

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Load chunks.json for search data
with open("data/chunks.json", "r", encoding="utf-8") as f:
    chunks_data = json.load(f)

# Load ToC map for fixed section filters
with open("data/toc_map.json", "r", encoding="utf-8") as f:
    toc_map = json.load(f)

# Build document list
documents = sorted(set(chunk["document"] for chunk in chunks_data))

# Build fallback auto section map
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
    answer = ""
    selected_doc = ""
    selected_section = ""
    results = []

    if request.method == "POST":
        if "clear" in request.form:
            return render_template("index.html", question="", answer="", results=[], documents=documents, sections=[], selected_doc="", selected_section="")

        question = request.form.get("question", "")
        selected_doc = request.form.get("document", "")
        selected_section = request.form.get("section", "")

        if question:
            try:
                results = get_answer(question, selected_doc, selected_section)
                answer = "Check-Mate’s Response"
            except Exception as e:
                logging.exception("Error during answer processing")
                results = []
                answer = f"An error occurred: {str(e)}"

    # Use ToC if available, else fallback to derived sections
    if selected_doc in toc_map:
        sections = toc_map[selected_doc]
    else:
        sections = sorted(document_sections.get(selected_doc, set())) if selected_doc else []

    return render_template(
        "index.html",
        question=question,
        answer=answer,
        results=results,
        documents=documents,
        sections=sections,
        selected_doc=selected_doc,
        selected_section=selected_section
    )

if __name__ == "__main__":
    app.run(debug=True)
