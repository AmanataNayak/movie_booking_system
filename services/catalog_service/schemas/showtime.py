# schemas/showtime.py
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import UUID

class ShowtimeBase(BaseModel):
    start_time: datetime
    end_time: datetime

class ShowtimeCreate(ShowtimeBase):
    movie_id: UUID
    auditorium_id: UUID

class ShowtimeUpdate(ShowtimeBase):
    pass

class ShowtimeOut(ShowtimeBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)