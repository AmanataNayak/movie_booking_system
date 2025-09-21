from pydantic import BaseModel, UUID4, ConfigDict
from typing import Optional
from schemas.genre import GenreOut

class MovieBase(BaseModel):
    title: str
    description: Optional[str] = None
    poster_image_url: Optional[str] = None
    duration_minutes: Optional[int] = None

class MovieCreate(MovieBase):
    genre_ids: list[UUID4] = []
    show_time_ids: list[UUID4] = []

class MovieUpdate(MovieBase):
    genre_ids: Optional[list[UUID4]] = None
    show_time_ids: Optional[list[UUID4]] = None

class MovieOut(MovieBase):
    id: UUID4
    genres: list[GenreOut] = []
    model_config = ConfigDict(from_attributes=True)