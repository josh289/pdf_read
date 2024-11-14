from flask import Flask, request
from main import summarize_pdf

app = Flask(__name__)

@app.route('/extract-pdf', methods=['POST'])
def extract_pdf():
    response = summarize_pdf(request)
    if isinstance(response, tuple):
        return response
    return response

if __name__ == '__main__':
    app.run(debug=True, port=8080) 