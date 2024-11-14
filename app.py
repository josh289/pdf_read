import os
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
    port = int(os.getenv("PORT", default=5000))
    app.run(host='0.0.0.0', debug=False, port=port) 