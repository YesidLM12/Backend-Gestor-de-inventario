
from typing import Optional
from pydantic import BaseModel, EmailStr
from app.utils.enums import UserRole


class UserBase(BaseModel):
    email: EmailStr
    username: str
    role: Optional[UserRole]

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username: str
    role: Optional[UserRole]
    is_active: bool