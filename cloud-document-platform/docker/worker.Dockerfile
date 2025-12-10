FROM python:3.11-slim

WORKDIR /app

COPY services/worker/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

# Set PYTHONPATH to /app so 'worker.py' is importable
ENV PYTHONPATH=/app

# Celery command
CMD ["celery", "-A", "services.worker.worker", "worker", "--loglevel=info"]

