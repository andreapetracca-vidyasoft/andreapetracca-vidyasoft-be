import uuid
from sqlalchemy import ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.sqltypes import DateTime
from app.connection import Base
from app.schemas.Book import Book
from app.schemas.User import User


class Booking(Base):
    __tablename__ = "bookings"
    __table_args__ = (
        Index("idx_bookings_user_id", "user_id"),
        Index("idx_bookings_book_id", "book_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    book_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("books.id", ondelete="RESTRICT"), nullable=False
    )

    booking_date: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    return_date: Mapped[DateTime] = mapped_column(DateTime, nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="bookings")
    book: Mapped["Book"] = relationship("Book", back_populates="bookings")
