from celery import Celery
from services.worker.worker_config import CeleryConfig

celery = Celery("worker")
celery.config_from_object(CeleryConfig)

celery.autodiscover_tasks(['services.worker.tasks'])
