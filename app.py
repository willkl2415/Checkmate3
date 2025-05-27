from flask import Flask, render_template, request
from answer_engine import answer_question
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", response="")

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.form["query"]

    try:
        results = answer_question(user_input)
        if results:
            answer = ""
            for match in results:
                answer += f"<strong>{match['document']} | {match['heading']}</strong><br>{match['content']}<br><br>"
        else:
            answer = "No results found in JSP 822 Vol 2 for your query."
    except Exception as e:
        answer = f"An error occurred: {str(e)}"

    return render_template("index.html", response=answer)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
