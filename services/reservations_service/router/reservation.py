from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas.reservation import ReservationBase, ReservationOut
from services.reservations import hold_reservation, confirm_reservation, cancel_reservation, list_available_seats
from common.iam import get_current_user, TokenData

router = APIRouter(
    prefix="/reservations",
    tags=["Reservation"],
    dependencies=[Depends(get_current_user)]
)

@router.post("/hold", response_model=ReservationOut)
def hold(reservation: ReservationBase, db: Session = Depends(get_db), user: TokenData = Depends(get_current_user)):
    return hold_reservation(db, user.user_id, reservation)

@router.post("/{reservation_id}/confirm", response_model=ReservationOut)
def confirm(reservation_id: str, db: Session = Depends(get_db), user: TokenData = Depends(get_current_user)):
    return confirm_reservation(db, reservation_id, user.user_id)

@router.post("/{reservation_id}/cancel", response_model=ReservationOut)
def cancel(reservation_id: str, db: Session = Depends(get_db), user: TokenData = Depends(get_current_user)):
    return cancel_reservation(db, reservation_id, user.user_id)

@router.get("/{showtime_id}/available-seats")
def available_seats(showtime_id: str, db: Session = Depends(get_db)):
    return list_available_seats(db, showtime_id)

