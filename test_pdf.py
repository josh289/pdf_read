from main import summarize_pdf
import base64
from flask import Request
from werkzeug.test import EnvironBuilder
import json

def test_pdf_extraction():
    # Use the specific PDF file
    pdf_path = 'testPDF.pdf'
    
    # Read and encode the PDF
    with open(pdf_path, 'rb') as file:
        pdf_base64 = base64.b64encode(file.read()).decode('utf-8')
    
    # Create mock request
    builder = EnvironBuilder(
        method='POST',
        json={'pdf': pdf_base64}
    )
    mock_request = Request(builder.get_environ())
    
    # Call the function
    response = summarize_pdf(mock_request)
    
    # Print the result
    if isinstance(response, tuple):
        response_data, status_code = response
        print(f"Status Code: {status_code}")
        print("Response:", json.dumps(response_data, indent=2))
    else:
        print("Response:", json.dumps(response, indent=2))

if __name__ == "__main__":
    test_pdf_extraction() 