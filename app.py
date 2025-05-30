from flask import Flask, render_template, request
from answer_engine import get_answer
import json
import os

app = Flask(__name__)

# Load section headings and documents from chunks.json
with open("chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

documents = sorted(list(set(chunk["document"] for chunk in chunks)))
sections = sorted(list(set(chunk["heading"] for chunk in chunks)))

@app.route("/", methods=["GET", "POST"])
def index():
    response = ""
    selected_document = ""
    selected_section = ""
    if request.method == "POST":
        query = request.form.get("query", "")
        selected_document = request.form.get("document", "")
        selected_section = request.form.get("section", "")
        if query:
            response = get_answer(query, selected_document, selected_section)
    return render_template(
        "index.html",
        response=response,
        documents=documents,
        sections=sections,
        selected_document=selected_document,
        selected_section=selected_section
    )

# ✅ Render-compatible port binding
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
