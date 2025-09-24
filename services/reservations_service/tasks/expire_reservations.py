from celery import Celery
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from services.reservations import expire_reservations
from database import get_db

celery_app = Celery(
    "reservation_tasks",
    broker="redis://host.docker.internal:6379/0",
    backend="redis://host.docker.internal:6379/0"
)

@celery_app.task
def expire_reservations_task():
    db: Session = next(get_db())
    expire_reservations(db, datetime.utcnow())
