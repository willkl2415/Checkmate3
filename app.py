from flask import Flask, render_template, request
import json
import os

app = Flask(__name__)

# Load chunks from the correct data directory
CHUNKS_PATH = os.path.join("data", "chunks.json")

try:
    with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
        chunks = json.load(f)
except FileNotFoundError:
    chunks = []
    print(f"ERROR: Cannot find {CHUNKS_PATH}. Please ensure the file exists.")

@app.route("/")
def index():
    return render_template("index.html", response="")

@app.route("/ask", methods=["POST"])
def ask():
    query = request.form.get("query", "").lower()
    if not query:
        return render_template("index.html", response="Please enter a question.")

    try:
        results = []
        for chunk in chunks:
            content = chunk.get("content", "").lower()
            if query in content:
                results.append(chunk)

        if results:
            response = ""
            for match in results:
                document = match.get("document", "Unknown")
                heading = match.get("heading", "No heading")
                content = match.get("content", "")
                response += f"<strong>{document} | {heading}</strong><br>{content}<br><br>"
        else:
            response = "No matching results found in the documents."

    except Exception as e:
        response = f"An error occurred: {str(e)}"

    return render_template("index.html", response=response)

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=10000)
