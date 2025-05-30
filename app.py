from flask import Flask, render_template, request
from answer_engine import get_answer

import json

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    response = ""
    selected_document = None
    selected_section = None

    if request.method == "POST":
        query = request.form.get("query", "").strip()
        selected_document = request.form.get("document") or None
        selected_section = request.form.get("section") or None

        if query:
            results = get_answer(query, selected_document, selected_section)
            if results:
                formatted = ""
                for item in results:
                    formatted += f"<strong>{item['document']} – {item['section']}</strong><br>{item['content']}<br><br>"
                response = formatted
            else:
                response = "<strong>No relevant information found in the selected documents.</strong>"

    return render_template("index.html", response=response)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=10000)
