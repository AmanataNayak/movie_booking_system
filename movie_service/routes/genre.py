from fastapi import APIRouter, Depends
from database import get_db
from services.genre import *
from schemas.genre import *
from sqlalchemy.orm import Session


router = APIRouter(prefix="/genres", tags=["Genre"])

@router.post("/", response_model=GenreOut)
def create_genres(genre: GenerCreate, db: Session = Depends(get_db)):
    return create_genre(db, genre)


@router.get("/{genre_name}", response_model=GenreOut)
def get_genre(genre_name: str, db: Session = Depends(get_db)):
    return get_genre_by_names(db, genre_name)

@router.get("/", response_model=list[GenreOut])
def get_all_genres(db: Session = Depends(get_db)):
    return get_genres(db)
