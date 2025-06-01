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
            results = get_answer(question, selected_doc, selected_section)
            answer = "Check-Mate’s Response"

    sections = sorted(document_sections.get(selected_doc, set())) if selected_doc else []
    return render_template("index.html", question=question, answer=answer, results=results, documents=documents, sections=sections, selected_doc=selected_doc, selected_section=selected_section)

if __name__ == "__main__":
    app.run(debug=True)
