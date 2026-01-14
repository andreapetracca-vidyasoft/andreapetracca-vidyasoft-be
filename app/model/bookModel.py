import uuid
from typing import Optional
from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    author: str
    genre: str


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    genre: Optional[str] = None


class BookRead(BookBase):
    id: uuid.UUID

    model_config = {
        "from_attributes": True
    }
