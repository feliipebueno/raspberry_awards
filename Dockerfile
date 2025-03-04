# Etapa 1: Build
FROM python:3.12-slim AS builder
LABEL maintainer="Felipe Bueno <felipe.bueno@safelabs.com>"
LABEL version="1.0"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y gcc musl-dev && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN python -m pip install --upgrade pip

COPY requirements.txt .
RUN pip install -r requirements.txt && rm -rf /root/.cache

COPY . /app

# Etapa 2: Final
FROM python:3.12-slim AS final
LABEL maintainer="Felipe Bueno <felipe.bueno@safelabs.com>"
LABEL version="1.0"

RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/opt/venv/bin:$PATH"

COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app /app

RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 7000

CMD [ "sh", "-c", "alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port 7000"]
