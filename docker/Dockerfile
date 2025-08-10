# Use modern Python base image
FROM python:3.12-slim

# Install system dependencies with cleanup
RUN apt-get update && apt-get install -y \
    curl \
    postgresql-client \
    python3-tk \
    tk-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir fastapi uvicorn && \
    python -m spacy download en_core_web_sm

# Copy application code
COPY src/ ./src/
COPY config/ ./config/
COPY scripts/ ./scripts/
COPY main.py ./
COPY .env* ./

# Create necessary directories with proper permissions
RUN mkdir -p data/sources data/outputs/logs data/outputs/visualizations && \
    chmod 755 data/sources data/outputs/logs data/outputs/visualizations

# Expose ports
EXPOSE 8000 8001

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Use non-root user for security
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

# Health check (following Docker best practices)
HEALTHCHECK --interval=10s --timeout=5s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the FastAPI server
CMD ["python", "main.py"] 