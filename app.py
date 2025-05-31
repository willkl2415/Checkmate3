from flask import Flask, render_template, request
from answer_engine import get_answer
import json
import os

app = Flask(__name__)

# Load document chunks
with open("data/chunks.json", "r", encoding="utf-8") as f:
    chunks_data = json.load(f)

# Document and section indexing for dropdowns
documents = sorted(set(chunk["document"] for chunk in chunks_data))
document_sections = {}
for chunk in chunks_data:
    doc = chunk["document"]
    section = chunk.get("heading", "Uncategorised")
    if doc not in document_sections:
        document_sections[doc] = set()
    document_sections[doc].add(section)
for doc in document_sections:
    document_sections[doc] = sorted(document_sections[doc])

@app.route("/", methods=["GET", "POST"])
def index():
    query = ""
    selected_doc = ""
    selected_section = ""
    results = []
    show_filter_hint = False

    if request.method == "POST":
        query = request.form.get("query", "").strip()
        selected_doc = request.form.get("document", "").strip()
        selected_section = request.form.get("section", "").strip()

        if query:
            results = get_answer(query, selected_doc, selected_section)
            show_filter_hint = len(results) > 10

    return render_template(
        "index.html",
        response=results,
        query=query,
        documents=documents,
        document_sections=document_sections,
        selected_doc=selected_doc,
        selected_section=selected_section,
        show_filter_hint=show_filter_hint
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(debug=True, host="0.0.0.0", port=port)
