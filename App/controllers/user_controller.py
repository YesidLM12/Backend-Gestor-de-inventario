from sqlalchemy.orm import Session
from app.controllers.base_controller import BaseController
from app.models.user import User
from app.schemas.user_schema import UserCreate
from app.utils.enums import UserRole
from app.core.security import verify_password, ger_password_hash
from fastapi import HTTPException, status
import jwt

class UserController(BaseController):

    @staticmethod
    def create_user(db: Session, user: UserCreate) -> User:

        existing_user = db.query(User).filter((User.username == user.username) | (User.email == user.email)).first()

        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User already exists')

        hashed_password = ger_password_hash(user.password)
        user.password = hashed_password

        db_user = User(
            email=user.email,
            username=user.username,
            role=user.role,
            password=hashed_password
        )

        db.add(db_user)

        return db_user
    
    @staticmethod
    def update_user(db: Session, user_id: int, user: User) -> User:
        return super().update(db, user_id, user)
    
    @staticmethod
    def delete_user(db: Session, user_id: int) -> User:
        return super().delete(db, user_id)
    
    @staticmethod
    def get_multi(db: Session, skip: int = 0, limit: int = 100):
        return super().get_multi(db, skip, limit)
    
    @staticmethod
    def get_by_id(db: Session, user_id: int) -> User:
        return super().get_by_id(db, user_id)
    
    def get_by_role(db: Session, role: UserRole) -> list[User]:
        return db.query(User).filter(User.role == role).all()
    
    def update_role(db: Session, user_id: int, new_role: UserRole):
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

        user.role = new_role.role
        db.add(user)
        db.commit()

        return user 

    @staticmethod
    def get_by_email(db: Session, email: str):
        return db.query(User).filter(User.email == email).first()
    

    def authenticate(db: Session, email:str, password: str):
        user = UserController.get_by_email(db, email)

        if not user or not verify_password(password, user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')
        return user