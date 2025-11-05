from functools import wraps
from typing import Callable
from fastapi import HTTPException, status
from app.api.deps import get_current_user
from app.utils.enums import UserRole
from jose import jwt, JWTError
from app.core.config import settings    

PERMISSIONS = {
    'ADMIN': ['*'],
    'MANAGER': ['read:*', 'write:inventory', 'write:suppliers'],
    'OPERATOR': ['read:inventory', 'write:movements'],
    'VIEWER': ['read:*']
}


def has_permission(user: dict, action: str) -> bool:
    role = user['role']
    permissions = PERMISSIONS.get(role, [])

    if '*' in permissions:
        return True

    if action in permissions:
        return True

    for per in permissions:
        if perm.endswith('*') and action.startswith(per.split(':')[0]):
            return True

    return False


def require_role(*required_role: UserRole):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            current_user: User = kwargs.get('current_user')

            if not current_user:
                from fastapi import Depends
                current_user = Depends(get_current_user)

            if current_user.role not in required_role:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail='Not enough permissions')

            return await func(*args, **kwargs)
        return wrapper
    return decorator


def require_permission(action: str):
    """Decorator to check if the user has the required permission
    example:
    @require_permission('write:inventory')
    """

    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request: Request = kwargs.get('request')
            user = get_current_user(request)

            if not has_permission(user, action):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail='Not enough permissions')

            return await func(*args, **kwargs)
        return wrapper
    return decorator
