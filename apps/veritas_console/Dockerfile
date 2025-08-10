FROM python:3.12-slim
WORKDIR /app
COPY apps/veritas_console/requirements.txt requirements.txt
RUN pip install -U pip && pip install -r requirements.txt && pip install streamlit
COPY apps/veritas_console/ .
CMD ["streamlit","run","app.py","--server.port=8501","--server.address=0.0.0.0"]

