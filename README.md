# PDF Text Extractor API

A FastAPI-based service that extracts text from PDF documents. The service accepts base64-encoded PDF files and returns the extracted text in a structured format.

## Features

- Asynchronous PDF text extraction
- Efficient text splitting for large documents
- Health check endpoint
- OpenAPI documentation
- Docker support
- Railway deployment ready

## Prerequisites

- Python 3.11+
- Docker (optional)
- poppler-utils (for PDF processing)

## Installation

1. Clone the repository:
git clone <repository-url>
cd pdf-extractor

2. Install dependencies:
pip install -r requirements.txt

3. Run locally:
python app.py

## Testing

1. Test local API:
python test_pdf.py

2. Test deployed API:
python test_deployed_api.py

Example test code:
```python
import requests
import base64

def test_deployed_api():
    # Read and encode the PDF
    with open('testPDF.pdf', 'rb') as file:
        pdf_base64 = base64.b64encode(file.read()).decode('utf-8')

    # Make request to the correct endpoint with HTTPS
    url = "https://pdfread-production.up.railway.app/extract-pdf"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "pdf": pdf_base64
    }

    # Make the POST request
    response = requests.post(url, json=payload, headers=headers, verify=True)

    # Print results
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("Success! Extracted text:")
        print(response.json()['full_text'])
    else:
        print("Error:")
        print(response.json())

if __name__ == "__main__":
    test_deployed_api()
```

## Docker Deployment

Build and run with Docker:
docker build -t pdf-extractor .
docker run -p 5000:5000 pdf-extractor

## API Documentation

- Swagger UI: /docs
- ReDoc: /redoc

## Deployment

The service is configured for deployment on Railway.app. Make sure to:
1. Use HTTPS for all API calls
2. Set appropriate environment variables
3. Configure the PORT variable in Railway

Important: When testing deployed version, always use HTTPS to prevent POST requests from being converted to GET requests.
