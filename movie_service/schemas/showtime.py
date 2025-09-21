from pydantic import BaseModel, UUID4, ConfigDict
from datetime import datetime

class ShowTimeBase(BaseModel):
    start_time: datetime
    end_time: datetime

class ShowTimeCreate(ShowTimeBase):
    pass

class ShowTimeUpdate(ShowTimeBase):
    pass

class ShowTimeOut(ShowTimeBase):
    id: UUID4
    movie_id: UUID4

    model_config = ConfigDict(from_attributes=True)
