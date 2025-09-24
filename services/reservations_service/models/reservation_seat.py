from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
import uuid
from database import Base


class ReservationSeat(Base):
    __tablename__ = "reserved_seats"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    reservation_id = Column(UUID(as_uuid=True), ForeignKey("reservations.id", ondelete="CASCADE"), nullable=False)
    seat_id = Column(UUID(as_uuid=True), nullable=False)

    __table_args__ = (
        # no double booking for same seat in same reservation
        UniqueConstraint('reservation_id', 'seat_id', name='uq_reservation_seat'),
    )

    