from flask import Flask, render_template, request
from answer_engine import answer_question

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', response="Awaiting your question...")

@app.route('/ask', methods=['POST'])
def ask():
    query = request.form['query']
    try:
        results = answer_question(query)
        if results:
            formatted_results = ""
            for match in results:
                formatted_results += f"<strong>{match['document']} | {match['heading']}</strong><br>{match['content']}<br><br>"
        else:
            formatted_results = "No matching results found in the documents."
    except Exception as e:
        formatted_results = f"An error occurred: {str(e)}"
    return render_template('index.html', response=formatted_results)

if __name__ == '__main__':
    app.run(debug=True)
