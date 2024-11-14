# Use Python 3.9 slim image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Run the application with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:${PORT:-5000}", "--workers", "4", "--timeout", "120", "app:app"] 