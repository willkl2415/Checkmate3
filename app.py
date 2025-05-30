from flask import Flask, render_template, request
import json
from answer_engine import get_answer

app = Flask(__name__)

with open("chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

documents = sorted(set(chunk["document"] for chunk in chunks))

document_sections = {}
for chunk in chunks:
    doc = chunk["document"]
    heading = chunk["heading"]
    if doc not in document_sections:
        document_sections[doc] = []
    if heading not in document_sections[doc]:
        document_sections[doc].append(heading)

@app.route("/", methods=["GET", "POST"])
def index():
    response = ""
    question = ""
    selected_document = ""
    selected_heading = ""

    if request.method == "POST":
        question = request.form.get("question", "").strip()
        selected_document = request.form.get("document", "")
        selected_heading = request.form.get("section", "")
        response = get_answer(question, selected_document, selected_heading)

    return render_template(
        "index.html",
        response=response,
        question=question,
        documents=documents,
        document_sections=document_sections,
        selected_document=selected_document,
        selected_heading=selected_heading,
    )

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
