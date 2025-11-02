
from fastapi import APIRouter
from sqlalchemy.orm import Session
from app.api.v1.routes.users_route import create_user
from app.schemas.token_schema import Token
from app.core.security import create_access_token, login_for_access_token
from app.controllers.user_controller import UserController
from fastapi.security import OAuth2PasswordRequestForm
from app.core.dependencies import get_db
from fastapi import Depends
from app.schemas.user_schema import UserCreate, UserResponse
from fastapi import HTTPException, status
from datetime import timedelta

router = APIRouter()

@router.post('/register', response_model=UserResponse)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        existing_user = UserController.get_by_email(db, user.email)

        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email already exists')

        new_user = UserController.create_user(db, user)

        db.commit()
        db.refresh(new_user)
        
        access_token = create_access_token(data={"sub": new_user.email}, expires_delta=timedelta(minutes=15))
        return {'User': new_user, 'access_token': access_token, 'token_type': 'bearer'}   
    except Exception as e:
        db.rollback()
        print(f'Error al crear el usuario: {e}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post('/login', response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = UserController.authenticate(db, form_data.username, form_data.password)
    return login_for_access_token(user.email, user.password)
