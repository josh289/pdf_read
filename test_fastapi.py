import asyncio
import base64
import httpx
import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_extract_pdf():
    # Read and encode the PDF
    with open('testPDF.pdf', 'rb') as file:
        pdf_base64 = base64.b64encode(file.read()).decode('utf-8')
    
    # Make request
    response = client.post(
        "/extract-pdf",
        json={"pdf": pdf_base64}
    )
    
    # Check response
    assert response.status_code == 200
    data = response.json()
    assert "full_text" in data
    assert len(data["full_text"]) > 0

async def test_async_performance():
    """Test multiple concurrent requests"""
    async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
        # Read and encode the PDF
        with open('testPDF.pdf', 'rb') as file:
            pdf_base64 = base64.b64encode(file.read()).decode('utf-8')
        
        # Make multiple concurrent requests
        tasks = []
        for _ in range(3):  # Test with 3 concurrent requests
            tasks.append(
                ac.post("/extract-pdf", json={"pdf": pdf_base64})
            )
        
        # Wait for all requests to complete
        responses = await asyncio.gather(*tasks)
        
        # Check all responses
        for response in responses:
            assert response.status_code == 200
            data = response.json()
            assert "full_text" in data
            assert len(data["full_text"]) > 0

if __name__ == "__main__":
    pytest.main([__file__]) 