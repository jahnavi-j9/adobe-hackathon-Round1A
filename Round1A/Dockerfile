FROM --platform=linux/amd64 python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY models/ ./models/

# Set Python path
ENV PYTHONPATH=/app/src

# Create input/output directories
RUN mkdir -p /app/input /app/output

# Run the application
CMD ["python", "src/main.py"]
