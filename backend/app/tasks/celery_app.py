from celery import Celery
import logging
from app.core.config import get_settings

logger = logging.getLogger("app.tasks.celery_app")

settings = get_settings()

# Choose a safe broker if none provided (memory broker is suitable for local/dev only)
broker = settings.CELERY_BROKER_URL or "memory://"
backend = settings.CELERY_RESULT_BACKEND or None

if not settings.CELERY_BROKER_URL:
    logger.warning("CELERY_BROKER_URL not set; falling back to in-memory broker (dev only)")

# Initialize Celery with safe defaults
celery_app = Celery(
    "spacescope",
    broker=broker,
    backend=backend,
)

celery_app.conf.update(
    task_serializer=getattr(settings, "CELERY_TASK_SERIALIZER", "json"),
    accept_content=getattr(settings, "CELERY_ACCEPT_CONTENT", ["json"]),
    result_serializer=getattr(settings, "CELERY_RESULT_SERIALIZER", "json"),
    timezone=getattr(settings, "CELERY_TIMEZONE", "UTC"),
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
)

# Import tasks to register them (keeps the same behavior)
from app.tasks import (
    ingest_api_data,
    run_ml_inference,
    periodic_updates,
)
