
from datetime import timedelta
from datetime import datetime
import bcrypt
from fastapi import HTTPException, status
import pyjwt as jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.dependencies import settings
from app.controllers.user_controller import UserController

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__default_rounds=12, bcrypt__default_ident='2b')


def verify_password(plain_password:str, hashed_password:str) -> bool:
    password_bytes = plain_password.encode('utf-8')[:72]
    return bcrypt.hashpw(password_bytes, hashed_password.encode('utf-8'))

def ger_password_hash(password: str) -> str:
    password_bytes = password.encode('utf-8')[:72]
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password_bytes, salt).decode('utf-8')

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

def login_for_access_token(db: Session, email: str, password: str):

    user = UserController.get_by_email(db,email)

    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")

    access_token_expire = timedelta(minutes=15)
    return {"access_token": create_access_token(data={"sub": user.email}, expires_delta=access_token_expire), "token_type": "bearer"}



