FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py retrieval.py ./

COPY knowledge/ ./knowledge/

RUN groupadd --gid 10001 appgroup \
    && useradd --no-log-init --uid 10001 \
    --gid 10001 --no-create-home appuser

USER appuser

HEALTHCHECK --interval=10s --timeout=3s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/ready',timeout=2).close()"

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]