from sqlalchemy.orm import Session
from uuid import UUID
from models.genres import Genre
from models.movies import Movie
from models.showtimes import ShowTime
from schemas.movie import *

def get_movie(db: Session, movie_id: UUID) -> Movie | None:
    return db.query(Movie).filter(Movie.id == movie_id).first()

def get_movies(db: Session, limit: int = 500) -> list[type[Movie]]:
    return db.query(Movie).limit(limit).all()

def create_movie(db: Session, movie: MovieCreate) -> Movie:
    db_movie = Movie(
        title=movie.title,
        description=movie.description,
        poster_image_url=movie.poster_image_url,
        duration_minutes=movie.duration_minutes
    )

    for gener_id in movie.genre_ids:
        gener = db.query(Genre).filter(Genre.id == gener_id).first()
        if gener:
            db_movie.genres.append(gener)

    for show_time_id in movie.show_time_ids:
        show_time = db.query(Genre).filter(ShowTime.id == show_time_id).first()
        if show_time:
            db_movie.genres.append(show_time)

    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie


def delete_movie(db: Session, movie_id: UUID) -> Movie | None:
    """Deletes a movie"""
    db_movie = get_movie(db, movie_id)
    if not db_movie:
        return None
    db.delete(db_movie)
    db.commit()
    return db_movie

def update_movie(db: Session, movie_id: UUID, movie_update: MovieUpdate) -> Movie | None:
    db_movie = db.query(Movie).filter(Movie.id == movie_id).first()

    if not db_movie:
        return None

    for column, value in movie_update.model_dump(exclude_unset=True).items():
        if column != "genre_ids" or column != "show_time_ids":
            setattr(db_movie, column, value)

    if movie_update.genre_ids is not None:
        db_movie.geners.clear()
        for gener_id in movie_update.genre_ids:
            gener = db.query(Genre).filter(Genre.id == gener_id).first()
            if gener:
                db_movie.geners.append(gener)

    if movie_update.show_time_ids is not None:
        db_movie.showtimes.clear()
        for show_time_id in movie_update.show_time_ids:
            show_time = db.query(ShowTime).filter(ShowTime.id == show_time_id).first()
            if show_time:
                db_movie.showtimes.append(show_time)

    db.commit()
    db.refresh(db_movie)
    return db_movie

def extend_genres(db: Session, movie_id: UUID, genre_id: UUID) -> Movie | None:
    """Add new genres to a movie"""
    genre = db.query(Genre).filter(Genre.id == genre_id).first()
    movie = db.query(Movie).filter(Movie.id == movie_id).first()

    if genre:
        movie.genres.append(genre)
    elif genre is None or movie is None:
        return None

    db.commit()
    db.refresh(movie)
    return movie
