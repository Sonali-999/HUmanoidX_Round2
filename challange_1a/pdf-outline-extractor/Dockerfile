# Use a lightweight base image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Install system dependencies required by PyMuPDF
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libgl1-mesa-glx \
 && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire codebase
COPY . .

# Default command to run your script
CMD ["python", "main.py"]
