# Use official Python (lightweight, CPU-only)
FROM python:3.10-slim

WORKDIR /app

# System dependencies for PyMuPDF
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential gcc && \
    rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code, data, etc.
COPY . .

# Make sure output directory exists
RUN mkdir -p output

# Run main pipeline
CMD ["python", "main.py"]
