from flask import Flask, render_template, request
from answer_engine import get_answer
import json
import os

app = Flask(__name__)

# Load chunks
with open("data/chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

# Prepare document and section filters
documents = sorted(set(chunk["document"] for chunk in chunks))
sections = sorted(set(chunk.get("section", "Uncategorised") for chunk in chunks))

@app.route("/", methods=["GET", "POST"])
def index():
    answer = ""
    question = ""
    document = ""
    section = ""
    trimmed = False
    document_shown = ""

    if request.method == "POST":
        question = request.form.get("question", "")
        document = request.form.get("document", "")
        section = request.form.get("section", "")
        results, trimmed = get_answer(question, document, section)
        answer = "\n\n".join(results)
        document_shown = document if document else ""

    return render_template(
        "index.html",
        answer=answer,
        question=question,
        documents=documents,
        sections=sections,
        result_count=answer.count("Result "),
        trimmed=trimmed,
        document_shown=document_shown
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
