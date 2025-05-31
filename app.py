import os
from flask import Flask, render_template, request
from answer_engine import get_answer

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    answer = ""
    question = ""
    selected_document = ""
    selected_section = ""

    if request.method == "POST":
        question = request.form.get("question", "").strip()
        selected_document = request.form.get("document", "").strip()
        selected_section = request.form.get("section", "").strip()
        answer = get_answer(question, selected_document, selected_section)

    # List documents from /docs folder
    docs_folder = "docs"
    documents = [f for f in os.listdir(docs_folder) if f.endswith(".docx")]

    # Static list for sections — not active but kept for layout
    sections = ["All sections", "N/A"]

    return render_template(
        "index.html",
        answer=answer,
        question=question,
        documents=documents,
        sections=sections
    )

if __name__ == "__main__":
    app.run(debug=True)
