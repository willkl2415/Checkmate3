from flask import Flask, render_template, request
from answer_engine import get_answer
import json
import os

app = Flask(__name__)

with open("chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

@app.route("/", methods=["GET", "POST"])
def index():
    response = []
    query = ""
    selected_document = ""
    selected_section = ""

    if request.method == "POST":
        query = request.form.get("query", "")
        selected_document = request.form.get("document", "")
        selected_section = request.form.get("section", "")

        if query:
            response = get_answer(chunks, query, selected_document, selected_section)

    # Extract unique document names and section names for filters
    documents = sorted(set(chunk["document"] for chunk in chunks))
    sections = sorted(set(chunk["heading"] for chunk in chunks))

    return render_template(
        "index.html",
        response=response,
        query=query,
        documents=documents,
        sections=sections,
        selected_document=selected_document,
        selected_section=selected_section
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # ✅ Corrected for Render
    app.run(debug=True, host="0.0.0.0", port=port)
