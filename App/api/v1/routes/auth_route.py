from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserLogin
from app.core.dependencies import get_db
from app.core.security import verify_password, create_access_token, hash_password
from fastapi import HTTPException
from app.api.deps import get_current_admin_or_manager

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
async def register(user: UserCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_or_manager)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User already exists"
        )
    hashed_password = hash_password(user.password)

    if user.role == "admin":
        user.is_admin = True
    else:
        user.is_admin = False
        
    db_user = User(
        full_name=user.full_name,
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        role=user.role,
        is_admin=user.is_admin,
        is_active=True
    )
    db.add(db_user)
    db.commit()
    return {"message": "Register successful"}
