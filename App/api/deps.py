
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi import status
import jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.dependencies import get_db
from app.core.security import oauth2_scheme
from app.utils.enums import UserRole
from app.models.user_model import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except Exception:
        raise credentials_exception

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

    


async def get_current_admin(current_user: User = Depends(get_current_user)):

    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    return current_user


async def get_current_manager(current_user: User = Depends(get_current_user)):

    if current_user.role != UserRole.MANAGER:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    return current_user


async def get_current_admin_or_manager(current_user: User = Depends(get_current_user)):

    if current_user.role != UserRole.ADMIN and current_user.role != UserRole.MANAGER:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    return current_user