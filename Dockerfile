FROM python:3.12-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


FROM python:3.12-slim AS runtime

WORKDIR /app

COPY --from=builder /install /usr/local

COPY src/ ./src/
COPY alembic/ ./alembic/
COPY alembic.ini .

ENV DATABASE_URL="" \
    SECRET_KEY="" \
    PORT=8000 \
    PYTHONPATH=/app

EXPOSE ${PORT}

CMD ["sh", "-c", "uvicorn src.main:app --host 0.0.0.0 --port ${PORT}"]
