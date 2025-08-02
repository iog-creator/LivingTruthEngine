# Use modern Python base image
FROM python:3.12-slim

# Install system dependencies with cleanup
RUN apt-get update && apt-get install -y \
    curl \
    postgresql-client \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir fastapi uvicorn

# Copy application code
COPY src/ ./src/
COPY config/ ./config/
COPY .env* ./

# Create necessary directories with proper permissions
RUN mkdir -p data/sources data/outputs/logs data/outputs/visualizations && \
    chmod 755 data/sources data/outputs/logs data/outputs/visualizations

# Create a simple FastAPI server with health check
RUN echo 'from fastapi import FastAPI\n\
from fastapi.middleware.cors import CORSMiddleware\n\
import uvicorn\n\
\n\
app = FastAPI(title="Living Truth Engine", version="1.0.0")\n\
\n\
# Add CORS middleware\n\
app.add_middleware(\n\
    CORSMiddleware,\n\
    allow_origins=["*"],\n\
    allow_credentials=True,\n\
    allow_methods=["*"],\n\
    allow_headers=["*"],\n\
)\n\
\n\
@app.get("/health")\n\
async def health_check():\n\
    return {"status": "healthy", "service": "Living Truth Engine"}\n\
\n\
@app.get("/")\n\
async def root():\n\
    return {"message": "Living Truth Engine API", "status": "operational"}\n\
\n\
@app.get("/dashboard")\n\
async def dashboard():\n\
    return {"message": "Dashboard endpoint", "status": "ready"}\n\
\n\
if __name__ == "__main__":\n\
    uvicorn.run(app, host="0.0.0.0", port=8000)' > /app/main.py

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