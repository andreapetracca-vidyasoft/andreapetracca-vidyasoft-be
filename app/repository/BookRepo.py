import uuid
from sqlalchemy.orm import Session
from app.schemas.Book import Book


class BookRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, book: Book) -> Book:
        self.db.add(book)
        self.db.commit()
        self.db.refresh(book)
        return book

    def get_all(self) -> list[Book]:
        return self.db.query(Book).all()

    def get_by_id(self, user_id: uuid.UUID) -> Book | None:
        return self.db.query(Book).filter(Book.id == user_id).first()

    def update(self, user_id: uuid.UUID, updated_user: Book) -> Book | None:
        book = self.db.query(Book).filter(Book.id == user_id).first()
        if not book:
            return None

        for key, value in updated_user.__dict__.items():
            setattr(book, key, value)

        self.db.commit()
        self.db.refresh(book)
        return book

    def delete(self, user_id: uuid.UUID) -> bool:
        book = self.db.query(Book).filter(Book.id == user_id).first()
        if not book:
            return False

        self.db.delete(book)
        self.db.commit()
        return True
