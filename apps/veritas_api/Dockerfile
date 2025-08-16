FROM python:3.12-slim
WORKDIR /app
# When build context is repo root, copy only this app's requirements and code
COPY apps/veritas_api/requirements.txt requirements.txt
RUN pip install -U pip && pip install -r requirements.txt
COPY apps/veritas_api/ .
CMD ["uvicorn","main:app","--host","0.0.0.0","--port","8080"]

