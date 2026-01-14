import uuid
from sqlalchemy.orm import Session
from app.schemas.User import User


class UserRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_all(self) -> list[User]:
        return self.db.query(User).all()

    def get_by_id(self, user_id: uuid.UUID) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def update(self, user_id: uuid.UUID, updated_user: User) -> User | None:
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return None

        for key, value in updated_user.__dict__.items():
            setattr(user, key, value)

        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user_id: uuid.UUID) -> bool:
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return False

        self.db.delete(user)
        self.db.commit()
        return True
