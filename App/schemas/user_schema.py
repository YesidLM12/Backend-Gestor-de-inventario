
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from app.utils.enums import UserRole
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    username: str
    role: Optional[UserRole] = None

class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=72)

class UserUpdate(UserBase):
    password: str = Field(min_length=8, max_length=72)

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username: str
    role: str
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class RegisterResponse(BaseModel):
    User: UserResponse
    access_token: str
    token_type: str