# app.py
import os
from flask import Flask, render_template, request
from answer_engine import get_answer
import json

app = Flask(__name__)

with open("data/chunks.json", "r", encoding="utf-8") as f:
    chunks_data = json.load(f)

documents = sorted(set(chunk["document"] for chunk in chunks_data))

@app.route("/", methods=["GET", "POST"])
def index():
    primary_question = ""
    refined_query = ""
    selected_document = ""
    answer = []

    if request.method == "POST":
        primary_question = request.form.get("question", "").strip()
        refined_query = request.form.get("refine", "").strip()
        selected_document = request.form.get("document", "")

        filters = {}
        if selected_document and selected_document != "All Documents":
            filters["document"] = selected_document

        query_to_use = refined_query if refined_query else primary_question
        answer = get_answer(query_to_use, filters)

    return render_template(
        "index.html",
        documents=documents,
        answer=answer,
        question=primary_question,
        refine=refined_query,
        selected_document=selected_document,
        total_results=len(answer)
    )
