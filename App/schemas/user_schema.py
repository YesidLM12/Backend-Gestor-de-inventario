
from typing import Optional
from pydantic import BaseModel, EmailStr, constr
from app.utils.enums import UserRole
from datetime import datetime

# Schema para crear un usuario
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: Optional[UserRole] = None 


# Schema para mostrar un usuario
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: Optional[UserRole] = None
    is_active: bool


class UserInBD(UserResponse):
    hashed_password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None

