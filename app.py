import os
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from main import extract_pdf_text, split_text
import base64

app = FastAPI(
    title="PDF Text Extractor",
    description="API for extracting text from PDF documents",
    version="1.0.0"
)

class PDFRequest(BaseModel):
    pdf: str
    
    class Config:
        schema_extra = {
            "example": {
                "pdf": "base64_encoded_pdf_content"
            }
        }

class PDFResponse(BaseModel):
    full_text: str

class ErrorResponse(BaseModel):
    detail: str

@app.post("/extract-pdf", 
    response_model=PDFResponse,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    })
async def extract_pdf(request: PDFRequest):
    """
    Extract text from a base64 encoded PDF file.
    
    - **pdf**: Base64 encoded PDF content
    
    Returns the extracted text from all pages.
    """
    try:
        # Decode the base64 PDF
        try:
            pdf_data = base64.b64decode(request.pdf)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid base64 encoding: {str(e)}")

        # Extract text from the PDF asynchronously
        full_text = await extract_pdf_text(pdf_data)
        
        if not full_text.strip():
            raise HTTPException(status_code=400, detail="No text could be extracted from the PDF")
        
        # Split the text into parts based on character limits
        text_parts = split_text(full_text, max_chars=3000)
        
        # Join parts efficiently
        final_text = "\n".join(text_parts)
        
        return {"full_text": final_text}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", default=5000))
    uvicorn.run(app, host="0.0.0.0", port=port) 