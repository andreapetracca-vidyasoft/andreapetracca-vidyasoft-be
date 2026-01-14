import uuid
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    name: str
    email: EmailStr
    tax_id: str


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    tax_id: Optional[str] = None


class UserRead(UserBase):
    id: uuid.UUID

    model_config = {
        "from_attributes": True
    }
