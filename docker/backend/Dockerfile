FROM python:3.12-slim

WORKDIR /app

COPY backend/pyproject.toml backend/uv.lock ./

RUN pip install --no-cache-dir uv

RUN uv sync --frozen --no-dev