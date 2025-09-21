from zoneinfo import reset_tzpath

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from schemas.showtime import ShowTimeOut, ShowTimeCreate, ShowTimeUpdate
from services.showtime import *
from database import get_db
from uuid import UUID

router = APIRouter(prefix="/showtime", tags=["Showtime"])

@router.post("/{movie_id}", response_model=ShowTimeOut, status_code=status.HTTP_201_CREATED)
def create(movie_id: UUID, show_time: ShowTimeCreate, db: Session = Depends(get_db)):
    return create_showtime(db, movie_id, show_time)

@router.get("/movie/{movie_id}", response_model=list[ShowTimeOut])
def get_show_times(movie_id: UUID, db: Session = Depends(get_db)):
    return get_show_time_by_movie(db, movie_id)


@router.delete("/{showtime_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(showtime_id: UUID, db: Session = Depends(get_db)):
    showtime = delete_show_time(db, showtime_id)
    if showtime is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The showtime doesn't exist")


@router.put("/{showtime_id}", response_model=ShowTimeOut)
def update(showtime_id: UUID, showtime: ShowTimeUpdate, db: Session = Depends(get_db)):
    showtime = update_show_time(db, showtime_id, showtime)
    if showtime is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The showtime doesn't exist"
        )
    return showtime




