# app.py
import os
import json
from flask import Flask, render_template, request
from answer_engine import get_answer

app = Flask(__name__)

with open("data/chunks.json", "r", encoding="utf-8") as f:
    chunks_data = json.load(f)

documents = sorted(set(chunk["document"] for chunk in chunks_data))

@app.route("/", methods=["GET", "POST"])
def index():
    question = ""
    refine_query = ""
    answer = []

    if request.method == "POST":
        question = request.form.get("question", "").strip()
        selected_doc = request.form.get("document", "")
        refine_query = request.form.get("refine_query", "").strip()
        filters = {"document": selected_doc}
        combined_query = f"{question} {refine_query}".strip()
        answer = get_answer(combined_query, filters)

    return render_template(
        "index.html",
        question=question,
        refine_query=refine_query,
        documents=["All Documents"] + documents,
        selected_doc=request.form.get("document", "All Documents"),
        answer=answer
    )

if __name__ == "__main__":
    app.run(debug=True)
