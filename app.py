# app.py
import os
from flask import Flask, render_template, request, redirect
from answer_engine import get_answer
import json

app = Flask(__name__)

with open("data/chunks.json", "r", encoding="utf-8") as f:
    chunks_data = json.load(f)

documents = sorted(set(chunk["document"] for chunk in chunks_data))

@app.route("/", methods=["GET", "POST"])
def index():
    question = ""
    selected_doc = ""
    refine_query = ""
    answer = []

    if request.method == "POST":
        if "clear" in request.form:
            return redirect("/")
        question = request.form.get("question", "")
        selected_doc = request.form.get("document", "")
        refine_query = request.form.get("refine_query", "")

        filters = {
            "document": selected_doc,
            "refine_query": refine_query
        }

        answer = get_answer(question, filters)

    return render_template("index.html", question=question, selected_doc=selected_doc, refine_query=refine_query, answer=answer, documents=documents)

if __name__ == "__main__":
    app.run(debug=True)
