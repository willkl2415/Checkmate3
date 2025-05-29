from flask import Flask, render_template, request
from answer_engine import answer_question

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', response="")

@app.route('/ask', methods=['POST'])
def ask():
    query = request.form['query']
    try:
        results = answer_question(query)
        if results:
            answer = ""
            for result in results:
                answer += f"<strong>{result['document']} | {result['heading']}</strong><br>{result['content']}<br><br>"
        else:
            answer = "No matching results found in the documents."
    except Exception as e:
        answer = f"An error occurred: {str(e)}"
    return render_template('index.html', response=answer)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
