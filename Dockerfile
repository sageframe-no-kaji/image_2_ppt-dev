FROM python:3.11-slim

# Install system dependencies for PDF processing
RUN apt-get update && apt-get install -y \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Gradio
RUN pip install --no-cache-dir gradio>=4.0.0

# Copy application files
COPY make_ppt.py .
COPY app.py .

# Create temp directory with proper permissions
RUN mkdir -p /tmp/pptx_builder && chmod 777 /tmp/pptx_builder

# Expose Gradio port
EXPOSE 7860

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:7860')"

# Run the Gradio app
CMD ["python", "app.py"]
