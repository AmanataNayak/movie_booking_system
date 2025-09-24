from sqlalchemy import Column, String, Integer, Enum, TIMESTAMP
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import UUID
import uuid
import enum
from database import Base

class ReservationStatus(str, enum.Enum):
    hold = "hold"
    confirmed = "confirmed"
    cancelled = "cancelled"
    expired = "expired"



class Reservations(Base):
    __tablename__ = "reservations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    showtime_id = Column(UUID(as_uuid=True), nullable=False)
    status = Column(Enum(ReservationStatus), nullable=False)
    created_at = Column(TIMESTAMP, server_default="NOW()")

