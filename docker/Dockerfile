FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create a simple health check endpoint
RUN echo 'import time; print("Living Truth Engine starting..."); time.sleep(3600)' > /app/placeholder.py

CMD ["python", "/app/placeholder.py"] 