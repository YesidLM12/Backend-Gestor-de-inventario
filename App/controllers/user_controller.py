from sqlalchemy.orm import Session
from app.models.user import User
from app.utils.enums import UserRole
from app.utils.security import verify_password
from fastapi import HTTPException, status

def get_by_role(db: Session, role: UserRole):
    return db.query(User).filter(User.role == role.role).all()

def update_role(db: Session, user_id: int, new_role: UserRole):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

    user.role = new_role.role
    db.add(user)
    db.commit()

    return user 

def get_by_email(db: Session, email: str):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    return user

def authenticate(db: Session, email:str, pasword: str):
    user = get_by_email(db, email)

    if not user or not verify_password(pasword, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')
    return user