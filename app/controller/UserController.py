import uuid
from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.connection import connect
from app.model.userModel import UserCreate, UserRead, UserUpdate
from app.repository.UserRepo import UserRepository
from app.schemas.User import User


router = APIRouter(prefix="/users", tags=["Users"])


class UserController:
    @router.get("/v1", response_model=List[UserRead], status_code=status.HTTP_200_OK)
    def get_all(db: Session = Depends(connect)):
        return UserRepository(db).get_all()

    @router.get("/v1/{Id}", response_model=UserRead, status_code=status.HTTP_200_OK)
    def get_by_id(Id: uuid.UUID, db: Session = Depends(connect)):
        user = UserRepository(db).get_by_id(Id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        return user

    @router.post("/v1", response_model=UserRead, status_code=status.HTTP_201_CREATED)
    def create_user(body: UserCreate, db: Session = Depends(connect)):
        return UserRepository(db).create(User(**body.model_dump()))

    @router.put("/v1/{Id}", response_model=UserRead, status_code=status.HTTP_200_OK)
    def update_user(Id: uuid.UUID, body: UserUpdate, db: Session = Depends(connect)):
        existing = UserRepository(db).get_by_id(Id)
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return UserRepository(db).update(Id, User(**body.model_dump(exclude_unset=True)))

    @router.delete("/v1/{Id}", status_code=status.HTTP_204_NO_CONTENT)
    def delete(Id: uuid.UUID, db: Session = Depends(connect)):
        if not UserRepository(db).delete(Id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
