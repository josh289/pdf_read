import os
from main import summarize_pdf
import base64
from flask import Request
from werkzeug.test import EnvironBuilder

def test_pdf_file(pdf_path):
    print(f"\nTesting PDF: {pdf_path}")
    print("-" * 50)
    
    try:
        # Create mock request
        with open(pdf_path, 'rb') as file:
            pdf_base64 = base64.b64encode(file.read()).decode('utf-8')
        
        builder = EnvironBuilder(
            method='POST',
            json={'pdf': pdf_base64}
        )
        mock_request = Request(builder.get_environ())
        
        # Process PDF
        response = summarize_pdf(mock_request)
        
        # Print results
        if isinstance(response, tuple):
            response_data, status_code = response
            print(f"Status Code: {status_code}")
            print("Response:", response_data.get_json())
        else:
            print("Response:", response.get_json())
            
    except Exception as e:
        print(f"Error processing {pdf_path}: {str(e)}")

def test_multiple_pdfs():
    # Directory containing PDF files
    pdf_dir = 'pdfs'  # Change this to your PDF directory
    
    # Test each PDF in the directory
    for filename in os.listdir(pdf_dir):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(pdf_dir, filename)
            test_pdf_file(pdf_path)

if __name__ == "__main__":
    test_multiple_pdfs() 