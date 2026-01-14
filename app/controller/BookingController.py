import uuid
from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status
from app.connection import connect
from app.model.bookingModel import BookingCreate, BookingRead
from app.schemas.Booking import Booking
from app.repository.BookingRepo import BookingRepository

router = APIRouter(prefix="/bookings", tags=["Bookings"])


class BookingController:

    @router.get("/v1", response_model=List[BookingRead], status_code=status.HTTP_200_OK)
    def get_all(db: Session = Depends(connect)):
        return BookingRepository(db).get_all()

    @router.get("/v1/{Id}", response_model=BookingRead, status_code=status.HTTP_200_OK)
    def get_by_id(Id: uuid.UUID, db: Session = Depends(connect)):
        repo = BookingRepository(db).get_by_id(Id)

        if not repo:
            return None

        return repo

    @router.get("/v1/user/{Id}",response_model=List[BookingRead],status_code=status.HTTP_200_OK,)
    def find_by_user(Id: uuid.UUID, db: Session = Depends(connect)):
        return BookingRepository(db).find_by_user(Id)

    @router.post("/v1", response_model=BookingRead, status_code=status.HTTP_201_CREATED)
    def create(body: BookingCreate, db: Session = Depends(connect)):
        return BookingRepository(db).create(Booking(**body.model_dump()))

    @router.put("/v1/{Id}", response_model=BookingRead, status_code=status.HTTP_200_OK)
    def update_booking(Id: uuid.UUID, body: BookingCreate, db: Session = Depends(connect)):
        if not BookingRepository(db).get_by_id(Id):
            return None

        return BookingRepository(db).update(Id, Booking(**body.model_dump()))

    @router.patch("/v1/{Id}/terminate",response_model=BookingRead,status_code=status.HTTP_200_OK,)
    def terminate_booking(Id: uuid.UUID, db: Session = Depends(connect)):
        if not BookingRepository(db).get_by_id(Id):
            return None

        return BookingRepository(db).terminate(Id)
