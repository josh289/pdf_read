# Use the Python 3 official image
FROM python:3

# Run in unbuffered mode
ENV PYTHONUNBUFFERED=1 

# Create and change to the app directory
WORKDIR /app

# Copy local code to the container image
COPY . ./

# Install project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the web service on container startup with our specific configurations
CMD gunicorn --bind "0.0.0.0:$PORT" --workers 4 --timeout 120 app:app 