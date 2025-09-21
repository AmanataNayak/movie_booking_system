from sqlalchemy import and_
from sqlalchemy.orm import Session
from schemas.showtime import ShowtimeCreate, ShowtimeUpdate
from models.showtime import Showtime
from uuid import UUID
from datetime import date, datetime

def get_showtime_by_id(db: Session, showtime_id: UUID) -> Showtime | None:
    return db.query(Showtime).filter(Showtime.id == showtime_id).first()

def create_showtime(db: Session, showtime: ShowtimeCreate) -> Showtime:
    showtime = Showtime(
        auditorium_id=showtime.auditorium_id,
        movie_id=showtime.movie_id,
        start_time=showtime.start_time,
        end_time=showtime.end_time
    )
    db.add(showtime)
    db.commit()
    db.refresh(showtime)
    return showtime


def delete_showtime(db: Session, showtime_id: UUID) -> Showtime | None:
    showtime = db.query(Showtime).filter(Showtime.id == showtime_id).first()
    if not showtime:
        return None
    db.delete(showtime)
    db.commit()
    return showtime

def list_of_showtime(db: Session, movie_id: UUID = None, show_date: date = None):
    query = db.query(Showtime)

    if movie_id:
        query = query.filter(Showtime.movie_id == movie_id)

    if show_date:
        # Filter for showtimes on the given date (ignoring time)
        start_of_day = datetime.combine(show_date, datetime.min.time())
        end_of_day = datetime.combine(show_date, datetime.max.time())
        query = query.filter(
            and_(
                Showtime.start_time >= start_of_day,
                Showtime.start_time <= end_of_day
            )
        )

    return query.order_by(Showtime.start_time).all()
