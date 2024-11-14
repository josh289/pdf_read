import os
import fitz  # PyMuPDF
import base64
import io
import json
import asyncio
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

async def extract_page_text(page):
    """Extract text from a single PDF page asynchronously."""
    try:
        # Run CPU-intensive text extraction in a thread pool
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, lambda: page.get_text("text") or "")
    except Exception as e:
        print(f"Error extracting text from page: {str(e)}")
        return ""

async def extract_pdf_text(pdf_data):
    """Extract text from the PDF data using async processing."""
    try:
        # Open PDF from memory buffer
        pdf_document = fitz.open(stream=pdf_data, filetype="pdf")
        
        # Create tasks for all pages
        tasks = [extract_page_text(pdf_document[i]) 
                for i in range(len(pdf_document))]
        
        # Process all pages concurrently
        texts = await asyncio.gather(*tasks)
        
        # Clean up
        pdf_document.close()
        
        return "\n".join(text.strip() for text in texts if text)
    except Exception as e:
        raise Exception(f"Error processing PDF: {str(e)}")

def split_text(text, max_chars=3000):
    """Split the text into smaller chunks more efficiently."""
    if not text:
        return []
    
    parts = []
    current_pos = 0
    text_length = len(text)
    
    while current_pos < text_length:
        if current_pos + max_chars >= text_length:
            parts.append(text[current_pos:])
            break
            
        # Find the last sentence boundary within the limit
        end_pos = current_pos + max_chars
        last_period = text.rfind('. ', current_pos, end_pos)
        
        if last_period != -1:
            parts.append(text[current_pos:last_period + 1])
            current_pos = last_period + 2
        else:
            # If no sentence boundary found, split at max_chars
            parts.append(text[current_pos:end_pos])
            current_pos = end_pos
            
    return parts

def summarize_pdf(request):
    """HTTP Cloud Function to extract and join parts of a PDF file."""
    try:
        request_json = request.get_json(silent=True)
        if not request_json:
            return {'error': 'No JSON data provided'}, 400

        pdf_base64 = request_json.get('pdf')
        if not pdf_base64:
            return {'error': 'No PDF provided'}, 400

        # Decode the base64 PDF
        try:
            pdf_data = base64.b64decode(pdf_base64)
        except Exception as e:
            return {'error': f'Invalid base64 encoding: {str(e)}'}, 400

        # Extract text from the PDF
        full_text = extract_pdf_text(pdf_data)
        
        if not full_text.strip():
            return {'error': 'No text could be extracted from the PDF'}, 400
        
        # Split the text into parts based on character limits
        text_parts = split_text(full_text, max_chars=3000)
        
        # Join parts efficiently
        final_text = "\n".join(text_parts)
        
        return {'full_text': final_text}
        
    except Exception as e:
        return {'error': f'Processing failed: {str(e)}'}, 500