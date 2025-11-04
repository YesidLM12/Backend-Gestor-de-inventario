from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserLogin
from app.core.dependencies import get_db
from app.core.security import verify_password, create_access_token, hash_password
from fastapi import HTTPException
from app.core.permissions import require_role
from app.utils.enums import UserRole

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login")
async def login(user: UserLogin, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if not existing_user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not verify_password(user.password, existing_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
    

@router.post("/register")
@require_role(UserRole.ADMIN)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User already exists"
        )
    hashed_password = hash_password(user.password)
    db_user = User(
        full_name=user.full_name,
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    return {"message": "Register successful"}
