from flask import Flask, render_template, request
import json
import os

app = Flask(__name__)

CHUNKS_FILE = os.path.join("data", "chunks.json")

def load_chunks():
    with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

@app.route("/")
def index():
    return render_template("index.html", response="")

@app.route("/ask", methods=["POST"])
def ask():
    query = request.form["query"].lower()
    try:
        chunks = load_chunks()
        matches = []

        for chunk in chunks:
            if query in chunk["content"].lower() or query in chunk["heading"].lower():
                matches.append(chunk)

        if matches:
            answer = ""
            for match in matches:
                answer += f"<strong>{match['document']} | {match['heading']}</strong><br>{match['content']}<br><br>"
        else:
            answer = "No matching results found in the documents."
    except Exception as e:
        answer = f"An error occurred: {str(e)}"

    return render_template("index.html", response=answer)

if __name__ == "__main__":
    app.run(debug=True)
