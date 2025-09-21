from fastapi import APIRouter, Depends, HTTPException, status, Query
from services.showtime import *
from schemas.showtime import *
from database import get_db
from sqlalchemy.orm import Session
from uuid import UUID
from utility.api_admin import admin_required_for_method


router = APIRouter(
    prefix="/showtimes",
    tags=["Showtimes"],
    dependencies=[Depends(admin_required_for_method(["POST", "PUT", "DELETE"]))]
)

@router.get("/filter", response_model=list[ShowtimeOut])
def list_showtimes(movie_id: str | None = Query(default=None), show_date: date = Query(default=date.today()),
    db: Session = Depends(get_db)
):
    return list_of_showtime(db, movie_id, show_date)

@router.post("/", response_model=ShowtimeOut, status_code=status.HTTP_201_CREATED)
def create(showtime: ShowtimeCreate, db: Session = Depends(get_db)):
    return create_showtime(db, showtime)


# Public get by ID
@router.get("/{showtime_id}", response_model=ShowtimeOut)
def get_one(showtime_id: UUID, db: Session = Depends(get_db)):
    showtime = get_showtime_by_id(db, showtime_id)
    if not showtime:
        raise HTTPException(status_code=404, detail="Showtime not found")
    return showtime

# Admin-only delete
@router.delete("/{showtime_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(showtime_id: UUID, db: Session = Depends(get_db)):
    showtime = delete_showtime(db, showtime_id)
    if not showtime:
        raise HTTPException(status_code=404, detail="Showtime not found")

