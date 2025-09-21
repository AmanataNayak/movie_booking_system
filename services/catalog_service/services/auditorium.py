from sqlalchemy.orm import Session
from schemas.auditorium import AuditoriumCreate, AuditoriumUpdate
from models.auditorium import Auditorium
from models.seat import Seat
from uuid import UUID

def get_auditorium_by_name(db: Session, auditorium_name: str) -> Auditorium | None:
    return db.query(Auditorium).filter(Auditorium.name == auditorium_name).first()

def get_auditorium(db: Session, auditorium_id: UUID) -> Auditorium | None:
    return db.query(Auditorium).filter(Auditorium.id == auditorium_id).first()

def get_auditoriums(db: Session, limit: int = 100) -> list[type[Auditorium]]:
    return db.query(Auditorium).limit(limit).all()

def create_auditorium(db: Session, auditorium: AuditoriumCreate) -> Auditorium | None:
    if get_auditorium_by_name(db, auditorium.name):
        return None

    db_auditorium = Auditorium(
        name = auditorium.name,
        total_seats = auditorium.rows * auditorium.seat_per_row
    )
    db.add(db_auditorium)
    db.commit()
    db.refresh(db_auditorium)

    for i in range(auditorium.rows):
        row_label = chr(65 + i)
        for seat_number in range(1, auditorium.seat_per_row+1):
            seat = Seat(auditorium_id=db_auditorium.id, row_label=row_label, seat_number=seat_number)
            db.add(seat)
    db.commit()

    return db_auditorium

def update_auditorium_name(db: Session, auditorium_id: UUID, auditorium_update: AuditoriumUpdate) -> Auditorium | None:
    db_auditorium = get_auditorium(db, auditorium_id)
    if not db_auditorium:
        return None
    for column, value in auditorium_update.model_dump().items():
        setattr(db_auditorium, column, value)

    db.commit()
    db.refresh(db_auditorium)
    return db_auditorium


def delete_auditorium(db: Session, auditorium_id: UUID) -> Auditorium | None:
    db_auditorium = get_auditorium(db, auditorium_id)
    if not db_auditorium:
        return None

    db.delete(db_auditorium)
    db.commit()
    return db_auditorium