from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi import HTTPException, status
from datetime import datetime, timedelta
from models.reservation import Reservations, ReservationStatus
from models.reservation_seat import ReservationSeat
from schemas.reservation import ReservationBase
from uuid import UUID
import datetime as dt

HOLD_TIMEOUT_MINUTES = 10

def hold_reservation(db: Session, user_id: UUID, reservation: ReservationBase) -> Reservations:
    db_reservation = Reservations(
        user_id = user_id,
        showtime_id = reservation.showtime_id,
        status = ReservationStatus.hold
    )

    db.add(db_reservation)
    db.flush()

    for seat_id in reservation.seat_ids:
        seat = ReservationSeat(reservation_id=db_reservation.id, seat_id=seat_id)
        db.add(seat)

    db.commit()
    db.refresh(seat)
    
    return db_reservation


def confirm_reservation(db: Session, reservation_id: UUID, user_id: UUID) -> Reservations:
    reservation = db.query(Reservations).filter(
            Reservations.id == reservation_id,
            Reservations.user_id == user_id,
            Reservations.status == ReservationStatus.hold
        ).first()

    if not reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reservation not found or not in hold state"
        )
    
    reservation.status = ReservationStatus.confirmed
    db.commit()
    return reservation


def cancel_reservation(db: Session, reservation_id: UUID, user_id: UUID) -> Reservations:
    reservation = db.query(Reservations).filter(
        Reservations.id == reservation_id,
        Reservations.user_id == user_id
    ).first()

    if not reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reservation not found"
        )
    
    seats = db.query(ReservationSeat).filter(
        ReservationSeat.reservation_id == reservation_id
    ).all()
    reservation.status = ReservationStatus.cancelled
    db.commit()
    seats = db.query(ReservationSeat).filter(
        ReservationSeat.reservation_id == reservation_id
    ).all()
    for seat in seats:
        db.delete(seat)
    db.commit()
    return reservation


def expire_old_reservations(db: Session):
    """Expire holds older than HOLD_TIMEOUT_MINUTES"""
    expiry_time = datetime.now(dt.UTC) - timedelta(minutes=HOLD_TIMEOUT_MINUTES)
    
    old_reservations = db.query(Reservations).filter(
        Reservations.status == ReservationStatus.hold,
        Reservations.created_at < expiry_time
    ).all()

    for r in old_reservations:
        r.status == ReservationStatus.expired

    db.commit()

def list_available_seats(db: Session, showtime_id: str):
    # all seats in auditorium of this showtime
    get_all_seat_sql = text("""
        SELECT s.id, s.row_label , s.seat_number FROM seats s
        JOIN auditoriums a ON a.id = s.auditorium_id
        JOIN showtimes st ON st.auditorium_id = a.id
        WHERE st.id = :showtime_id                  
    """)
    all_seats = db.execute(get_all_seat_sql, {"showtime_id": showtime_id}).fetchall()

    # reserved seats (not expired/cancelled)
    reserved_seat_sql = text("""
        SELECT rs.seat_id FROM reserved_seats rs
        JOIN reservations r ON r.id = rs.reservation_id
        WHERE r.showtime_id = :showtime_id
        AND r.status IN ('hold', 'confirmed')
    """)
    reserved = db.execute(reserved_seat_sql, {"showtime_id": showtime_id}).fetchall()

    reserved_ids = {r.seat_id for r in reserved}
    return [s for s in all_seats if s.id not in reserved_ids]
