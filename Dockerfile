# Digest oficial linux/amd64 consultado em 08/11/2026.
FROM python:3.12.16-slim-bookworm@sha256:0f086103b026048cc50cb5da25ec435c023c5241a83fc44daea593377abc61c4

LABEL org.opencontainers.image.title="TaskFlow API" \
      org.opencontainers.image.description="Laboratório acadêmico de CI/CD, tarefas e observabilidade" \
      org.opencontainers.image.source="https://github.com/Luiz-mnt/devops-taskflow"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    TASKFLOW_DB_PATH=/data/taskflow.db

WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN python -m pip install --no-cache-dir --disable-pip-version-check -r requirements.txt \
    && groupadd --gid 10001 taskflow \
    && useradd --uid 10001 --gid 10001 --no-create-home --home-dir /app --shell /usr/sbin/nologin taskflow \
    && install -d -o 10001 -g 10001 -m 0750 /data

COPY app/ ./app/
USER 10001:10001
EXPOSE 8000

HEALTHCHECK --interval=10s --timeout=3s --start-period=10s --retries=5 \
    CMD ["python", "-c", "import json, urllib.request; response = json.load(urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=2)); assert response == {'status': 'healthy', 'database': 'ok'}"]

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1", "--no-access-log"]
