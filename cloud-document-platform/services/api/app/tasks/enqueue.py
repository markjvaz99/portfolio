# services/api/app/tasks/enqueue.py
import requests
import json
import os
from celery import Celery

# For enqueueing we simply call Celery broker directly via python client in worker.
# But for decoupling, here we call a local HTTP webhook or Celery producer.
# Simpler: produce via redis pub, but for this skeleton we'll also create a Celery instance.

from celery import Celery
from app.core.config import settings

celery = Celery("producer", broker=settings.redis_url)

def enqueue_document_processing(doc_id: str, s3_key: str):
    # send a Celery task - assumes worker registered same task name
    celery.send_task("process_document", args=[doc_id, s3_key], queue="documents")
