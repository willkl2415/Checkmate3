# app.py
import os
import json
from flask import Flask, render_template, request, redirect, url_for
from answer_engine import get_answer

app = Flask(__name__)

# Load chunks.json
with open("data/chunks.json", "r", encoding="utf-8") as f:
    chunks_data = json.load(f)

# Get unique document names
documents = sorted(set(chunk["document"] for chunk in chunks_data))

@app.route("/", methods=["GET", "POST"])
def index():
    question = request.form.get("question", "").strip()
    selected_doc = request.form.get("document", "")
    refine_query = request.form.get("refine_query", "").strip()

    # Clear the search
    if request.form.get("clear") == "1":
        return redirect(url_for("index"))

    # Filter chunks by document
    filtered_chunks = [
        chunk for chunk in chunks_data
        if selected_doc in ("", "All Documents") or chunk["document"] == selected_doc
    ]

    # Refine the search results
    if refine_query:
        filtered_chunks = [
            chunk for chunk in filtered_chunks
            if refine_query.lower() in chunk["content"].lower()
        ]

    # Pass through question for matching
    answer = get_answer(question, filtered_chunks) if question else []

    return render_template(
        "index.html",
        answer=answer,
        question=question,
        documents=documents,
        selected_doc=selected_doc,
        refine_query=refine_query
    )

if __name__ == "__main__":
    app.run(debug=True)
