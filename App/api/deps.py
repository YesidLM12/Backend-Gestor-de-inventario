
from app.core.dependencies import get_current_user_from_request
from app.db.session import SessionLocal
from app.utils.enums import UserRole
from fastapi import Depends, HTTPException
from app.models.user import User
from app.utils.exceptions import PermissionDeniedException


def get_current_active_user(current_user: User = Depends(get_current_user_from_request)) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not active")
    return current_user


async def get_current_admin(current_user: User = Depends(get_current_user_from_request)):
    if current_user.role != UserRole.ADMIN.value.upper():
        raise PermissionDeniedException("Not enough permissions")
    return current_user


async def get_current_manager_or_admin(current_user: User = Depends(get_current_user_from_request)):
    if current_user.role != UserRole.ADMIN.value.upper() and current_user.role != UserRole.MANAGER.value.upper():
        raise PermissionDeniedException("Not enough permissions")
    return current_user