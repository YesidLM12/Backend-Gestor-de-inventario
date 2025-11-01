from fastapi import Depends, HTTPException, status
from typing import List
from app.utils.enums import UserRole
from jose import jwt, JWTError
from app.core.config import settings

PERMISSIONS = {
   'ADMIN': ['*'],
   'MANAGER': ['read:*', 'write:inventory', 'write:suppliers'],
   'OPERATOR': ['read:inventory', 'write:movements'],
   'VIEWER': ['read:*']
}

def get_current_user_from_request(request: Request):
    """Get the current user from the request"""

    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials')
    
    token = auth_header.split(' ')[1]

    try:

        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get('sub')
        role = payload.get('role')

        if not username or not role:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials')

        return {"username": username, "role": role}

    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials')


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
    
    def decorator(func: Callable):
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

    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request: Request = kwargs.get('request')
            user = get_current_user_from_request(request)

            if not has_permission(user, action):
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not enough permissions')

            return await func(*args, **kwargs)
        return wrapper
    return decorator