from functools import wraps
from fastapi import HTTPException, status
from app.utils.enums import UserRole
from jose import jwt, JWTError
from app.core.config import settings

PERMISSIONS = {
   'ADMIN': ['*'],
   'MANAGER': ['read:*', 'write:inventory', 'write:suppliers'],
   'OPERATOR': ['read:inventory', 'write:movements'],
   'VIEWER': ['read:*']
}

def has_permission(user:dict, action:str) -> bool:
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

def require_role(require_role: UserRole):
    """Decorator to check if the user has the required role
    example:
    @require_role(UserRole.ADMIN)
    """
    
    def decorator(func: callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request: Request = kwargs.get('request')
            user = get_current_user_from_request(request)

            if user['role'] != require_role.value.upper():
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not enough permissions')

            return await func(*args, **kwargs)
        return wrapper
    return decorator

def require_permission(action: str):
    """Decorator to check if the user has the required permission
    example:
    @require_permission('write:inventory')
    """

    def decorator(func:  callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request: Request = kwargs.get('request')
            user = get_current_user_from_request(request)

            if not has_permission(user, action):
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not enough permissions')

            return await func(*args, **kwargs)
        return wrapper
    return decorator