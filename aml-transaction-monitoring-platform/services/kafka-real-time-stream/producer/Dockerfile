FROM python:3.10-slim

WORKDIR /app

COPY services/kafka-real-time-stream/producer/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY services/kafka-real-time-stream/producer/producer.py .

CMD ["python", "producer.py"]
