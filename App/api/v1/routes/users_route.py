from fastapi import Router, Depends

from app.schemas.user import UserResponse
from app.controllers.user import update_role
from app.api.v1.dependencies import get_current_user
from app.utils.enums import UserRole

router = Router()

@router.put("/users/{user_id}/role", response_model=UserResponse)
async def update_user_role(user_id: int, new_role: UserRole, current_user: User = Depends(get_current_user)):
    return update_role(current_user.db, user_id, new_role)


