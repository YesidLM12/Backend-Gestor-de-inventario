
from typing import Optional
from pydantic import BaseModel, EmailStr, constr
from app.utils.enums import UserRole
from datetime import datetime

# Schema para crear un usuario


class UserCreate(BaseModel):
    full_name: str
    username: str
    email: EmailStr
    password: str
    role: Optional[UserRole] = "viewer"


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


class UserLogin(BaseModel):
    username: str
    password: str


class RoleUpdate(BaseModel):
    new_role: UserRole
