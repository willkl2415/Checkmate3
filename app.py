from flask import Flask, render_template, request
from answer_engine import answer_question

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    response = ""
    selected_doc = ""
    if request.method == "POST":
        query = request.form.get("query", "")
        selected_doc = request.form.get("document", "")
        if query:
            response = answer_question(query, selected_doc)
    return render_template("index.html", response=response)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=10000)
