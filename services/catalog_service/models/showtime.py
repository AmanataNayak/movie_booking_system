from sqlalchemy import Column, ForeignKey, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from database import Base
import uuid

class Showtime(Base):
    __tablename__ = "showtimes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    movie_id = Column(UUID(as_uuid=True), nullable=False)  # reference to Movie service
    auditorium_id = Column(UUID(as_uuid=True), ForeignKey("auditoriums.id", ondelete="CASCADE"), nullable=False)
    start_time = Column(TIMESTAMP(timezone=True), nullable=False)
    end_time = Column(TIMESTAMP(timezone=True), nullable=False)