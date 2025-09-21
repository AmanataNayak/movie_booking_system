from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from models.showtimes import ShowTime
from schemas.showtime import ShowTimeCreate, ShowTimeUpdate
from datetime import datetime, timedelta
from services.movie import get_movie

def validate_time_duration(movie_duration: int, start_time: datetime, end_time: datetime) -> bool:
    movie_duration = timedelta(minutes=movie_duration)
    actual_duration = end_time - start_time
    print(movie_duration)
    print(actual_duration)
    if actual_duration < movie_duration or actual_duration > movie_duration + timedelta(minutes=30):
        return False

    return True

def get_show_time_by_movie(db: Session, movie_id: UUID, limit: int = 30000) -> list[ShowTime]:
    return db.query(ShowTime).filter(ShowTime.movie_id == movie_id).limit(limit).all()

def create_showtime(db: Session, movie_id: UUID, show_time: ShowTimeCreate) -> ShowTime | None:
    movie_duration: int = get_movie(db, movie_id).duration_minutes
    if not validate_time_duration(movie_duration, show_time.start_time, show_time.end_time):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Showtime duration ({show_time.end_time - show_time.start_time}) does not match movie duration ({movie_duration})"
        )
    db_show_time = ShowTime(
        movie_id = movie_id,
        start_time = show_time.start_time,
        end_time = show_time.end_time
    )
    db.add(db_show_time)
    db.commit()
    db.refresh(db_show_time)
    return db_show_time


def delete_show_time(db: Session, show_time_id: UUID) -> ShowTime | None:
    db_show_time = db.query(ShowTime).filter(ShowTime.id == show_time_id).first()
    if not db_show_time:
        return None
    db.delete(db_show_time)
    db.commit()
    return db_show_time

def update_show_time(db: Session, show_time_id: UUID, show_time_update: ShowTimeUpdate) -> ShowTime | None:
    db_show_time = db.query(ShowTime).filter(ShowTime.id == show_time_id).first()
    if not db_show_time:
        return None
    movie_duration: int = get_movie(db, db_show_time.movie_id).duration_minutes
    if not validate_time_duration(movie_duration, show_time_update.start_time, show_time_update.end_time):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Showtime duration ({show_time_update.end_time - show_time_update.start_time}) does not match movie duration ({movie_duration})"
        )
    for column, value in show_time_update.model_dump(exclude_unset=True).items():
        setattr(db_show_time, column, value)

    db.commit()
    db.refresh(db_show_time)
    return db_show_time
