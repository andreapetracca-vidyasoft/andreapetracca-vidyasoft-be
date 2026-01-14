import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class BookingBase(BaseModel):
    book_id: uuid.UUID
    user_id: uuid.UUID


class BookingCreate(BookingBase):
    pass


class BookingUpdate(BaseModel):
    return_date: Optional[datetime] = None


class BookingClose(BaseModel):
    return_date: datetime


class BookingRead(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    book_id: uuid.UUID
    booking_date: datetime
    return_date: Optional[datetime]

    model_config = {
        "from_attributes": True
    }