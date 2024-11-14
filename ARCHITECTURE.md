# PDF Text Extractor - Architecture Overview

## Application Flow

1. **Request Handling**
   - FastAPI receives POST request at `/extract-pdf`
   - Request body is validated using Pydantic models
   - Base64-encoded PDF is extracted from request

2. **PDF Processing**
   ```
   Request → FastAPI → PDF Decoder → Text Extractor → Text Splitter → Response
   ```

3. **Testing**
```python
import requests
import base64

# 1. Prepare PDF data
with open('testPDF.pdf', 'rb') as file:
    pdf_base64 = base64.b64encode(file.read()).decode('utf-8')

# 2. Set up request
url = "https://pdfread-production.up.railway.app/extract-pdf"
headers = {
    "Content-Type": "application/json"
}
payload = {
    "pdf": pdf_base64
}

# 3. Make request
response = requests.post(url, json=payload, headers=headers, verify=True)

# 4. Handle response
if response.status_code == 200:
    print("Success! Extracted text:")
    print(response.json()['full_text'])
else:
    print("Error:", response.json())
```

4. **Component Details**

   a. **FastAPI Application** (`app.py`)
   - Handles HTTP requests
   - Validates input/output
   - Manages error handling
   - Provides API documentation

   b. **PDF Processing** (`main.py`)
   - `extract_pdf_text`: Async PDF text extraction
   - `extract_page_text`: Single page processing
   - `split_text`: Text chunking for large documents

   c. **Models**
   - `PDFRequest`: Input validation
   - `PDFResponse`: Output structure
   - `ErrorResponse`: Error handling

## Technical Architecture 

Client → FastAPI Endpoint → PDF Decoder → PDF Processor → Text Splitter → Response Handler

## Key Components

1. **HTTP Layer**
   - FastAPI framework
   - OpenAPI documentation
   - Request/Response validation

2. **Processing Layer**
   - Async PDF processing
   - Concurrent page extraction
   - Memory-efficient text handling

3. **Infrastructure**
   - Docker containerization
   - Railway deployment
   - Environment configuration

## Error Handling

1. **Input Validation**
   - PDF format validation
   - Base64 decoding checks
   - Size limits

2. **Processing Errors**
   - PDF parsing errors
   - Text extraction failures
   - Memory constraints

3. **HTTP Errors**
   - 400: Bad Request
   - 500: Server Error

## Testing Strategy

1. **Local Testing**
   - Use test_pdf.py for local API testing
   - Use test_multiple_pdfs.py for batch testing

2. **Deployment Testing**
   - Use test_deployed_api.py for testing deployed version
   - Always use HTTPS for deployed testing
   - Verify proper error handling

3. **Performance Testing**
   - Test with various PDF sizes
   - Test concurrent requests
   - Monitor memory usage