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
    selected_doc = request.form.get("document", "")
    selected_sections = request.form.getlist("section")
    refine_keywords = request.form.get("refine", "").split(",")

    if request.method == "POST":
        question = request.form.get("question", "")
        selected = [{"label": selected_doc}] if selected_doc else None
        answer = get_answer(question, selected, refine_keywords)

    return render_template(
        "index.html",
        answer=answer,
        question=question,
        documents=documents,
        document_sections=document_sections,
        selected_doc=selected_doc,
        selected_sections=selected_sections,
        refine_keywords=",".join(refine_keywords),
    )

if __name__ == "__main__":
    app.run(debug=True)
