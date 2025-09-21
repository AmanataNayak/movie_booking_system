import uuid
from sqlalchemy import Column, String, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from database import Base

class Seat(Base):
    __tablename__  = "seats"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    auditorium_id = Column(UUID(as_uuid=True), ForeignKey("auditoriums.id", ondelete="CASCADE"), nullable=False)
    row_label = Column(String(5), nullable=False)
    seat_number = Column(Integer, nullable=False)
    seat_type = Column(String, default="regular")

    __table_args__ = (
        # ensure unique seat per auditorium
        UniqueConstraint("auditorium_id", "row_label", "seat_number", name="uq_auditorium_seat"),
    )