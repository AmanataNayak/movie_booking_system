from sqlalchemy.orm import Session
from schemas.seat import SeatUpdate
from models.seat import Seat
from uuid import UUID

def get_seats_by_auditorium(db: Session, auditorium_id: UUID) -> list[type[Seat]]:
    return db.query(Seat).filter(Seat.auditorium_id == auditorium_id).order_by(Seat.row_label, Seat.seat_number).all()

def update_seat_type(db: Session, auditorium_id: UUID, seat_update: SeatUpdate) -> list[Seat] | None:
    seats = db.query(Seat).filter(
        Seat.auditorium_id == auditorium_id,
        Seat.row_label == seat_update.row_label
    ).all()

    if not seats:
        return None

    for seat in seats:
        seat.seat_type = seat_update.seat_type
    db.commit()
    return seats
