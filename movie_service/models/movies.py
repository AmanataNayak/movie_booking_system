import uuid
from sqlalchemy import Column, String, Text, Integer, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from database import Base
from models.genres import movie_genres_association

class Movie(Base):
    __tablename__ = "movies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    poster_image_url = Column(String, nullable=True)
    duration_minutes = Column(Integer, nullable=True)

    genres = relationship(
        'Genre',
        secondary=movie_genres_association,
        back_populates='movies'
    )

    showtimes = relationship(
        "ShowTime",
        back_populates="movies",
        cascade="all, delete"
    )