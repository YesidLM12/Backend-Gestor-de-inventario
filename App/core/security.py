
from datetime import timedelta
from datetime import datetime
from time import timezone
from typing import Optional
from fastapi import HTTPException, status
import jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from app.core.dependencies import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=[
                           "bcrypt"], deprecated="auto", bcrypt__default_rounds=12, bcrypt__default_ident='2b')


def hash_password(password: str) -> str:
    contraseña_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return contraseña_hash

    
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta

    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return encoded_jwt


def decode_token(token: str) -> dict:
    try:
        decoded_jwt = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        return decoded_jwt

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
