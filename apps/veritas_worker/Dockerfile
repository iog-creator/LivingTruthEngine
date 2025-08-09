FROM python:3.12-slim
WORKDIR /app
COPY apps/veritas_worker/requirements.txt requirements.txt
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*
RUN pip install -U pip && pip install -r requirements.txt
COPY apps/veritas_worker/ .
CMD ["python","worker.py"]

