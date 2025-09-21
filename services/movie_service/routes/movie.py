from fastapi import APIRouter, Depends, HTTPException, status
from services.movie import *
from schemas.movie import *
from database import get_db
from uuid import UUID
from sqlalchemy.orm import Session

router = APIRouter(prefix="/movies", tags=["Movie"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=MovieOut)
def create_movies(movie: MovieCreate, db: Session = Depends(get_db)):
    """Create a new movie"""
    return create_movie(db, movie)

@router.get("/", response_model=list[MovieOut])
def get_all_movies(db: Session = Depends(get_db)):
    return get_movies(db)


@router.get("/{movie_id}", response_model=MovieOut)
def get_movie_by_id(movie_id: UUID, db: Session = Depends(get_db)):
    movie = get_movie(db, movie_id)
    if movie is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie doesn't exist")
    return movie


@router.delete("/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_movie_by_id(movie_id: UUID, db: Session = Depends(get_db)):
    db_movie = delete_movie(db, movie_id)
    if db_movie is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie doesn't exist")


@router.put("/{movie_id}", response_model=MovieOut)
def update_movie_by_id(movie_id: UUID, movie: MovieUpdate, db: Session = Depends(get_db)):
    db_movie = update_movie(db, movie_id, movie)
    if db_movie is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie doesn't exist")
    return db_movie

@router.patch("/{movie_id}", response_model=MovieOut)
def add_genres(movie_id: UUID, genre_id: UUID, db: Session = Depends(get_db)):
    db_movie = extend_genres(db, movie_id, genre_id)
    if db_movie is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Details doesn't exist")
    return db_movie