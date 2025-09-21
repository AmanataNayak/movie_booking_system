from pydantic import BaseModel, ConfigDict, UUID4

class AuditoriumBase(BaseModel):
    name: str


class AuditoriumCreate(AuditoriumBase):
    rows: int
    seat_per_row: int

class AuditoriumUpdate(AuditoriumBase):
    pass

class AuditoriumOut(AuditoriumBase):
    id: UUID4
    name: str
    total_seats: int

    model_config = ConfigDict(from_attributes=True)

