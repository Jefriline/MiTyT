FROM node:20-alpine AS client_builder
WORKDIR /app

COPY Client/package*.json ./
RUN npm ci
COPY Client/ .
RUN npm run build:prod

FROM python:3.11-slim AS server_builder
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends gcc python3-dev && rm -rf /var/lib/apt/lists/*

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY server/requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gunicorn


FROM python:3.11-slim
WORKDIR /app

COPY --from=server_builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

RUN groupadd -r flaskgroup && useradd -r -g flaskgroup flaskuser

COPY server/ .
COPY --from=client_builder /app/static /Client/static
COPY Client/templates /Client/templates

RUN chown -R flaskuser:flaskgroup /app /Client /opt/venv
USER flaskuser

EXPOSE 5000


CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-5000} server:app --workers 4 --log-level debug"]
