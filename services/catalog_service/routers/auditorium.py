from fastapi import APIRouter, Depends, HTTPException, status
from services.auditorium import *
from schemas.auditorium import *
from database import get_db
from sqlalchemy.orm import Session
from uuid import UUID
from iam import admin_required_for_method


router = APIRouter(
    prefix="/auditoriums",
    tags=["Auditoriums"],
    dependencies=[Depends(admin_required_for_method(["POST", "PUT", "DELETE"]))]
)

@router.post("/", response_model=AuditoriumOut, status_code=status.HTTP_201_CREATED)
def create(auditorium: AuditoriumCreate, db: Session = Depends(get_db)):
    auditorium = create_auditorium(db, auditorium)
    if auditorium is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Auditorium already exist"
        )
    return auditorium


@router.get("/{auditorium_name}", response_model=AuditoriumOut)
def get_auditorium(auditorium_name: str, db: Session =  Depends(get_db)):
    auditorium = get_auditorium_by_name(db, auditorium_name)
    if auditorium is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No Auditorium found."
        )

    return auditorium

@router.get("/", response_model=list[AuditoriumOut])
def get_all_auditorium(db: Session = Depends(get_db)):
    return get_auditoriums(db)


@router.delete("/{auditorium_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(auditorium_id: UUID, db: Session = Depends(get_db)):
    auditorium = delete_auditorium(db, auditorium_id)

    if auditorium is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No auditorium found."
        )


@router.put("/{auditorium_id}", response_model=AuditoriumOut)
def delete(auditorium_id: UUID, auditorium: AuditoriumUpdate, db: Session = Depends(get_db)):
    auditorium = update_auditorium_name(db, auditorium_id, auditorium)

    if auditorium is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No auditorium found."
        )

    return auditorium
