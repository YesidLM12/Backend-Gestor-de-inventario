
from app.core.dependencies import get_current_user_from_request
from app.core.security import oauth2_scheme, jwt, settings
from app.db.session import SessionLocal
from app.schemas.user_schema import UserResponse
from app.utils.enums import UserRole
from fastapi import Depends, HTTPException
from app.utils.exceptions import PermissionDeniedException

def get_current_user(current_user: UserResponse = Depends(oauth2_scheme)) -> UserResponse:
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials')
    
    token = auth_header.split(' ')[1]
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get('sub')
        user_id = payload.get('id')
        role = payload.get('role')

        if not username or not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials')

        return {"username": username, "user_id": user_id, "role": role}

    except jwt.JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials')

def get_current_active_user(current_user: UserResponse = Depends(get_current_user_from_request)) -> UserResponse:
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not active")
    return current_user


async def get_current_admin(current_user: UserResponse = Depends(get_current_user_from_request)):
    if current_user.role != UserRole.ADMIN.value.upper():
        raise PermissionDeniedException("Not enough permissions")
    return current_user


async def get_current_manager_or_admin(current_user: UserResponse = Depends(get_current_user_from_request)):
    if current_user.role != UserRole.ADMIN.value.upper() and current_user.role != UserRole.MANAGER.value.upper():
        raise PermissionDeniedException("Not enough permissions")
    return current_user