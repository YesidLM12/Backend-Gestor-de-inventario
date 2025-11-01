from app.api.v1.endpoints import auth, users, suppliers, customers, raw_materials, inventory
from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(suppliers.router, prefix="/suppliers", tags=["suppliers"])
api_router.include_router(customers.router, prefix="/customers", tags=["customers"])
api_router.include_router(raw_materials.router, prefix="/raw_materials", tags=["raw_materials"])
api_router.include_router(inventory.router, prefix="/inventory", tags=["inventory"])
