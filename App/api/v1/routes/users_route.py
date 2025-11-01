from fastapi import Router, Depends

from app.core.permissions import require_role
from app.schemas.user import UserResponse
from app.controllers.user_controller import UserController
from app.api.v1.dependencies import get_current_user
from app.utils.enums import UserRole

router = Router()

@require_role(UserRole.ADMIN)
@router.put("/{user_id}/role", response_model=UserResponse)
async def update_user_role(user_id: int, new_role: UserRole, current_user: User = Depends(get_current_user)):
    return update_role(current_user.db, user_id, new_role)

@require_role(UserRole.ADMIN)
@router.get("/active", response_model=list[UserResponse])
async def get_active_users(current_user: User = Depends(get_current_user)):
    return UserController.get_active(current_user.db)



@require_role(UserRole.ADMIN)
@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(user_id: int, current_user: User = Depends(get_current_user)):
    return UserController.get_by_id(current_user.db, user_id)

@require_role(UserRole.ADMIN)
@router.get("/email/{email}", response_model=UserResponse)
async def get_user_by_email(email: str, current_user: User = Depends(get_current_user)):
    return UserController.get_by_email(current_user.db, email)

@require_role(UserRole.ADMIN)
@router.get("/search/{name}", response_model=list[UserResponse])
async def search_user_by_name(name: str, current_user: User = Depends(get_current_user)):
    return UserController.search_by_name(current_user.db, name)

@require_role(UserRole.ADMIN)
@router.get("/multi", response_model=list[UserResponse])
async def get_multi_users(skip: int = 0, limit: int = 100, current_user: User = Depends(get_current_user)):
    return UserController.get_multi(current_user.db, skip, limit)

@require_role(UserRole.ADMIN)
@router.get("/role/{role}", response_model=list[UserResponse])
async def get_users_by_role(role: UserRole, current_user: User = Depends(get_current_user)):
    return UserController.get_by_role(current_user.db, role)

@require_role(UserRole.ADMIN)
@router.delete("/{user_id}")
async def delete_user(user_id: int, current_user: User = Depends(get_current_user)):
    return UserController.delete(current_user.db, user_id)

@require_role(UserRole.ADMIN)
@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user: UserUpdate, current_user: User = Depends(get_current_user)):
    return UserController.update(current_user.db, user_id, user)

@require_role(UserRole.ADMIN)
@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate, current_user: User = Depends(get_current_user)):
    return UserController.create(current_user.db, user)

