# Use the Python 3 official image
FROM python:3

# Run in unbuffered mode
ENV PYTHONUNBUFFERED=1 

# Install system dependencies required for PyMuPDF
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libssl-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Create and change to the app directory
WORKDIR /app

# Copy local code to the container image
COPY . ./

# Install project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the web service on container startup
CMD uvicorn app:app --host 0.0.0.0 --port $PORT 