FROM python:3.11-alpine

# Install system dependencies for PDF processing and Python packages
RUN apk add --no-cache \
    poppler-utils \
    gcc \
    musl-dev \
    jpeg-dev \
    zlib-dev \
    libffi-dev

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

# Create non-root user
RUN adduser -D -u 1000 appuser && \
    mkdir -p /tmp && \
    chown -R appuser:appuser /app /tmp

# Switch to non-root user
USER appuser

# Expose Gradio port
EXPOSE 7860

# Run the Gradio app
CMD ["python", "app.py"]
