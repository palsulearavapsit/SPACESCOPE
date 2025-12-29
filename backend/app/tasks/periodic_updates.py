from celery.schedules import crontab
from app.tasks.celery_app import celery_app
from app.tasks import ingest_api_data


# Register periodic tasks
celery_app.conf.beat_schedule = {
    # Ingest NASA data every 6 hours
    "ingest-nasa-data": {
        "task": "app.tasks.ingest_api_data.ingest_nasa_data",
        "schedule": crontab(minute=0, hour="*/6"),
    },
    
    # Ingest space weather every 30 minutes
    "ingest-space-weather": {
        "task": "app.tasks.ingest_api_data.ingest_space_weather_data",
        "schedule": crontab(minute="*/30"),
    },
    
    # Predict solar activity daily at 00:00 UTC
    "predict-solar-activity": {
        "task": "app.tasks.ingest_api_data.predict_solar_activity",
        "schedule": crontab(minute=0, hour=0),
    },
    
    # Generate alerts every 2 hours
    "generate-event-alerts": {
        "task": "app.tasks.ingest_api_data.generate_event_alerts",
        "schedule": crontab(minute=0, hour="*/2"),
    },
}
