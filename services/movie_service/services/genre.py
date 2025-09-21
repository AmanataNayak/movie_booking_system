from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.genres import Genre
from schemas.genre import *

def get_genre_by_names(db: Session, name: str) -> Genre:
    """Fetch a gener by its name."""
    return db.query(Genre).filter(Genre.name == name).first()

def get_genres(db: Session, limit: int = 3000) -> list[type[Genre]]:
    """Fetch all genres"""
    return db.query(Genre).limit(limit).all()

def create_genre(db: Session, genre_create: GenerCreate):
    if get_genre_by_names(db, genre_create.name):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Genre with name: {genre_create.name} already exists.")

    db_genre = Genre(
        name=genre_create.name
    )
    db.add(db_genre)
    db.commit()
    db.refresh(db_genre)
    return db_genre

