import uuid
from sqlalchemy import Column, String,  Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from database import Base

# Association table for the many-to-many relationship
movie_genres_association = Table(
    'movie_genres', Base.metadata,
    Column('movie_id', UUID(as_uuid=True), ForeignKey('movies.id'), primary_key=True),
    Column('genre_id', UUID(as_uuid=True), ForeignKey('genres.id'), primary_key=True)
)



class Genre(Base):
    __tablename__ = 'genres'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False, index=True)

    movies = relationship(
        "Movie",
        secondary=movie_genres_association,
        back_populates="genres"
    )


