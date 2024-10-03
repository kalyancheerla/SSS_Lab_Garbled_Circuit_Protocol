FROM python:3.11-slim

RUN pip install --no-cache-dir faker kafka-python

WORKDIR /app
COPY producer.py .

CMD ["python", "./producer.py"]
