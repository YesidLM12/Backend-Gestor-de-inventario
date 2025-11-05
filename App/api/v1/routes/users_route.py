from fastapi import APIRouter, Depends

from app.controllers.user_controller import UserController
from app.core.permissions import require_role
from app.models.user_model import User
from app.schemas.user_schema import RoleUpdate, UserResponse, UserUpdate
from app.api.deps import get_current_admin, get_current_admin_or_manager, get_db, get_current_user
from app.utils.enums import UserRole
from sqlalchemy.orm import Session

router = APIRouter(prefix="/users", tags=["users"])


@router.put('/{user_id}/role', response_model=UserResponse)
async def update_user_role(
    user_id: int,
    role_update: RoleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
   user = UserController.update_role(db, user_id, role_update.new_role)

   if not user:
      raise HTTPException(status_code=404, detail="User not found")

   return user

@router.delete('/{user_id}', response_model=UserResponse)  
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    return UserController.delete(db, user_id)


@router.put('/{user_id}', response_model=UserResponse)
async def update_user(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    return UserController.update(db, user_id, user)



@router.get('/me', response_model=UserResponse)
async def read_current_user(current_user: User = Depends(get_current_user)):
    return UserController.get_user_me(current_user)


@router.get('/{user_id}', response_model=UserResponse)
async def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_or_manager)
):
    return UserController.get_user_by_id(db, user_id)


@router.get('/{email}', response_model=UserResponse)
async def get_user_by_email(
    email: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_or_manager)
):
    return UserController.get_user_by_email(db, email)

@router.get('/role/{role}', response_model=list[UserResponse])
async def get_user_by_role(
    role: UserRole,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    return UserController.get_user_by_role(db, role)


