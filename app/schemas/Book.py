import uuid
from typing import Literal
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.connection import Base

class Book(Base):
    __tablename__ = "books"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    
    title: Mapped[str] = mapped_column(nullable=False)
    author: Mapped[str] = mapped_column(nullable=False)
    genre: Mapped[Literal["Fiction", "Sci-Fi", "Romance", "History", "Thriller"]] = mapped_column(nullable=False)
    is_available: Mapped[bool] = mapped_column(default=True)

    bookings = relationship("Booking",back_populates="book",cascade="all, delete-orphan")
