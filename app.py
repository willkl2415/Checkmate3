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
    selected_doc = ""
    selected_section = ""

    if request.method == "POST":
        question = request.form["question"]
        selected_doc = request.form.get("document_filter", "")
        selected_section = request.form.get("section_filter", "")
        answer = get_answer(question, selected_doc, selected_section)

    return render_template("index.html", answer=answer, question=question,
                           documents=documents,
                           document_sections={k: sorted(v) for k, v in document_sections.items()},
                           selected_doc=selected_doc,
                           selected_section=selected_section)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)
