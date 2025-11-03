
from fastapi import Depends, HTTPException
import jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.dependencies import get_db
from app.core.security import oauth2_scheme
from app.utils.enums import UserRole
from app.models.user_model import User

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username = payload.get('sub')

        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")

    except Exception:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

    user = db.query(User).filter(User.username == username).first()

    if user is None:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

    return user


async def get_current_admin(current_user: User = Depends(get_current_user)):

    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    return current_user

async def get_current_manager(current_user: User = Depends(get_current_user)):

    if current_user.role != UserRole.MANAGER:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    return current_user