from flask import Flask, render_template, request
from answer_engine import answer_question

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
            answer = "No matching results found in the documents."
    except Exception as e:
        answer = f"An error occurred: {str(e)}"

    return render_template("index.html", response=answer)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
