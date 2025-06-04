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
    answer = []
    question = ""
    subquery = ""
    selected_doc = None

    if request.method == "POST":
        if request.form.get("clear"):
            return render_template("index.html", answer=[], question="", subquery="", documents=documents, selected_doc=None)

        question = request.form.get("question", "")
        subquery = request.form.get("subquery", "")
        selected_doc = request.form.get("document")

        filters = {"document": selected_doc}
        answer = get_answer(question, filters, subquery)

    return render_template("index.html", answer=answer, question=question, subquery=subquery, documents=documents, selected_doc=selected_doc)
