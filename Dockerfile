# Image for the FastAPI backend.

# Start from an official, small Python image.
FROM python:3.13-slim

# Don't write .pyc files, and print logs immediately (no buffering).
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies first, in their own layer. Docker caches each step, so as long as
# requirements.txt doesn't change, rebuilding after a code change skips this slow step.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

# Don't run as root inside the container: if the app is ever hacked, the attacker has fewer rights.
RUN useradd --create-home appuser
USER appuser

EXPOSE 8000

# 0.0.0.0 = accept connections from outside the container (127.0.0.1 would only allow the container itself).
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
