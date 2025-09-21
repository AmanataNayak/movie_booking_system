from pydantic import BaseModel, ConfigDict, UUID4

class SeatBase(BaseModel):
    seat_type: str

class SeatOut(SeatBase):
    id: UUID4
    row_label: str
    seat_number: int

    model_config = ConfigDict(from_attributes=True)

class SeatUpdate(SeatBase):
    row_label: str
