from celery import Celery
from app.config import settings


celery_app = Celery(
    "todo_app",
    broker=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
    include=[
        "app.background.email_jobs",
        "app.background.repeat_tasks"
    ]
)
