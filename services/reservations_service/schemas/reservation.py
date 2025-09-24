from pydantic import BaseModel, ConfigDict, UUID4
from models.reservation import ReservationStatus

class ReservationBase(BaseModel):
    showtime_id: UUID4
    seat_ids: list[UUID4]


class ReservationOut(BaseModel):
    id: UUID4
    user_id: UUID4
    showtime_id: UUID4
    status: ReservationStatus

    model_config = ConfigDict(from_attributes=True)
