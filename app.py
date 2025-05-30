from flask import Flask, render_template, request
from answer_engine import answer_question
import json

app = Flask(__name__)

@app.route("/")
def index():
    with open("chunks.json", "r", encoding="utf-8") as f:
        chunks = json.load(f)
    documents = sorted(set(chunk["document"] for chunk in chunks))
    sections = sorted(set(chunk["heading"] for chunk in chunks))
    return render_template("index.html", response="", document_filter="", section_filter="", documents=documents, sections=sections)

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.form.get("query", "")
    selected_document = request.form.get("document", "")
    selected_section = request.form.get("section", "")

    try:
        results = answer_question(user_input, selected_document, selected_section)
        if results:
            answer = ""
            for match in results:
                answer += f"<strong>{match['document']} | {match['heading']}</strong><br>{match['content']}<br><br>"
        else:
            answer = "No results found for your query."
    except Exception as e:
        answer = f"An error occurred: {str(e)}"

    with open("chunks.json", "r", encoding="utf-8") as f:
        chunks = json.load(f)
    documents = sorted(set(chunk["document"] for chunk in chunks))
    sections = sorted(set(chunk["heading"] for chunk in chunks))

    return render_template("index.html", response=answer, document_filter=selected_document, section_filter=selected_section, documents=documents, sections=sections)

if __name__ == "__main__":
    app.run(debug=True)
