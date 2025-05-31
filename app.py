import os
import json
from flask import Flask, render_template, request
from answer_engine import get_answer

app = Flask(__name__)

# Load section names from chunks.json
section_set = set()
try:
    with open("data/chunks.json", "r", encoding="utf-8") as f:
        chunks = json.load(f)
        for chunk in chunks:
            section = chunk.get("section", "Uncategorised")
            section_set.add(section)
except:
    section_set = {"Uncategorised"}

sections = sorted(section_set)

@app.route("/", methods=["GET", "POST"])
def index():
    answer = ""
    question = ""
    selected_document = ""
    selected_section = ""
    result_count = 0
    is_trimmed = False
    doc_display = ""

    if request.method == "POST":
        question = request.form.get("question", "").strip()
        selected_document = request.form.get("document", "").strip()
        selected_section = request.form.get("section", "").strip()
        answer, result_count, is_trimmed, doc_display = get_answer(
            question, selected_document, selected_section
        )

    docs_folder = "docs"
    documents = [f for f in os.listdir(docs_folder) if f.endswith(".docx")]

    return render_template(
        "index.html",
        answer=answer,
        question=question,
        documents=documents,
        sections=sections,
        result_count=result_count,
        trimmed=is_trimmed,
        document_shown=doc_display
    )

if __name__ == "__main__":
    app.run(debug=True)
