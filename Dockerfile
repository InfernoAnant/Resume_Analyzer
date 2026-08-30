# Multi-stage production Dockerfile
FROM python:3.12-slim AS builder

WORKDIR /app

# Prevent Python from writing .pyc and buffer stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Final runtime image
FROM python:3.12-slim

WORKDIR /app

# Non-root user for security best practice
RUN useradd -m -u 1000 appuser && \
    mkdir -p storage/uploads storage/reports storage/charts && \
    chown -R appuser:appuser /app

COPY --from=builder /install /usr/local
COPY --chown=appuser:appuser . /app

# Pre-download NLTK data into app environment
RUN python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

USER appuser

EXPOSE 5000

ENV PORT=5000
ENV FLASK_ENV=production

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--threads", "2", "app:app"]
