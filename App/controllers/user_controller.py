
from sqlalchemy.orm import Session

from app.controllers.base_controller import BaseController
from app.core.security import verify_password
from app.models.user_model import User
from app.schemas.user_schema import UserCreate
from fastapi import HTTPException

from app.utils.enums import UserRole


class UserController(BaseController):
    
    def get_user_by_email(self, db: Session, email:str):
        user = db.query(User).filter(User.email == email).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    

    def get_user_by_role(self, db: Session, role: UserRole):
        users = db.query(User).filter(User.role == role).all()

        if not users:
            raise HTTPException(status_code=404, detail="Users not found")
        return users
    

    def update_role(self, db: Session, user_id: int, new_role: UserRole):
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        user.role = new_role
        db.commit()
        return user
    
    def get_user_me(self, db: Session, current_user: User):
        user = db.query(User).filter(User.email == current_user.email).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    

    def create_user(self, db: Session, user: UserCreate):
        user = self.get_user_by_email(db, user.email)

        if user:
            raise HTTPException(status_code=400, detail="User already exists")
        
        try:
            user = User(
                email=user.email,
                hashed_password=hash_password(user.password)
            )

            print(f'User {user.email} created successfully')

            db.add(user)
            db.commit()
            db.refresh(user)
            return user

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    

    def authenticate_user(self, db: Session, email: str, password: str):
        user = self.get_user_by_email(db, email)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        if not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Incorrect password")
        
        return user