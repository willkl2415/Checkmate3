from flask import Flask, render_template, request
from answer_engine import answer_question
import os
import json

app = Flask(__name__)

# Load document metadata
with open("chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

documents = sorted(set(chunk["source"] for chunk in chunks))
sections_by_doc = {}
for chunk in chunks:
    doc = chunk["source"]
    sec = chunk.get("section", "Unknown")
    if doc not in sections_by_doc:
        sections_by_doc[doc] = set()
    sections_by_doc[doc].add(sec)
sections_by_doc = {doc: sorted(sections) for doc, sections in sections_by_doc.items()}


@app.route("/", methods=["GET", "POST"])
def index():
    response = ""
    question = ""
    selected_doc = ""
    selected_section = ""
    if request.method == "POST":
        question = request.form.get("question", "")
        selected_doc = request.form.get("document", "")
        selected_section = request.form.get("section", "")
        response = answer_question(question, selected_doc, selected_section)
    return render_template(
        "index.html",
        response=response,
        question=question,
        documents=documents,
        sections_by_doc=sections_by_doc,
        selected_doc=selected_doc,
        selected_section=selected_section,
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=10000)
