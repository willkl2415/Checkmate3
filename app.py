from flask import Flask, render_template, request
import answer_engine

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", response="")

@app.route("/ask", methods=["POST"])
def ask():
    query = request.form["query"]
    try:
        response = answer_engine.answer_question(query)
    except Exception as e:
        response = f"An error occurred: {str(e)}"
    return render_template("index.html", response=response)

if __name__ == "__main__":
    app.run()