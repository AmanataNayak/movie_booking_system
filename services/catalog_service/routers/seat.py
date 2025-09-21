from fastapi import APIRouter, HTTPException, Depends, status
from iam import admin_required_for_method
from services.seat import *
from schemas.seat import SeatOut, SeatUpdate
from uuid import UUID
from database import get_db

router = APIRouter(
    prefix="/seats",
    tags=["Seat"],
    dependencies=[Depends(admin_required_for_method(["POST", "PUT", "DELETE"]))]
)

@router.patch("/{auditorium_id}", response_model=list[SeatOut])
def update(auditorium_id: UUID, seat: SeatUpdate, db: Session = Depends(get_db)):
    seats = update_seat_type(db, auditorium_id, seat)
    if seat is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="seat doesn't exist"
        )
    return seats


@router.get("/{auditorium_id}", response_model=list[SeatOut])
def get_seats(auditorium_id: UUID, db: Session = Depends(get_db)):
    return get_seats_by_auditorium(db, auditorium_id)
