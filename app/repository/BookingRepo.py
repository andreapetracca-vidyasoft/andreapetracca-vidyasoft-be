import uuid
from datetime import datetime
from typing import List
from sqlalchemy.orm import Session
from app.schemas.Book import Book
from app.schemas.Booking import Booking


class BookingRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, booking: Booking) -> Booking:
        self.db.add(booking)
        self.db.commit()
        self.db.refresh(booking)
        return booking

    def get_all(self) -> list[Booking]:
        return self.db.query(Booking).all()

    def get_by_id(self, booking_id: uuid.UUID) -> Booking | None:
        return self.db.query(Booking).filter(Booking.id == booking_id).first()

    def find_by_user(self, user_id: uuid.UUID) -> List[Booking]:
        return self.db.query(Booking).filter(Booking.user_id == user_id).order_by(Booking.booking_date.desc()).all()

    def update(self, booking_id: uuid.UUID, updated_booking: Booking) -> Booking | None:
        booking = self.db.query(Booking).filter(Booking.id == booking_id).first()
        if not booking:
            return None

        for key, value in updated_booking.__dict__.items():
            setattr(booking, key, value)

        self.db.commit()
        self.db.refresh(booking)
        return booking

    def close(self, booking: Booking) -> Booking:
        if booking.return_date is not None:
            return booking

        booking.return_date = datetime.now()

        book = self.db.query(Book).filter(Book.id == booking.book_id).first()

        if book:
            book.is_available = True

        self.db.commit()
        self.db.refresh(booking)
        return booking
