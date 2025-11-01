
from pydantic import BaseModel
from app.utils.enums import UserRole

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    role: UserRole
    is_active: bool