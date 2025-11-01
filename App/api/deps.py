
from app.utils.enums import UserRole
from fastapi import Depends, HTTPException
from app.models.user import User
from app.utils.exceptions import PermissionDeniedException

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


async def get_current_admin(current_user: User = Depends(get_current_user_from_request)):
    if current_user.role != UserRole.ADMIN.value.upper():
        raise PermissionDeniedException("Not enough permissions")
    return current_user


async def get_current_manager_or_admin(current_user: User = Depends(get_current_user_from_request)):
    if current_user.role != UserRole.ADMIN.value.upper() and current_user.role != UserRole.MANAGER.value.upper():
        raise PermissionDeniedException("Not enough permissions")
    return current_user