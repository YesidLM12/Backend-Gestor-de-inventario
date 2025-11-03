from app.api.v1.routes import auth_route, users_route, suppliers_route
from fastapi import APIRouter

api_router = APIRouter()

# api_router.include_router(auth_route.router,prefix="/auth", tags=["auth"])
api_router.include_router(users_route.router)
api_router.include_router(suppliers_route.router)
# api_router.include_router(customers_route.router, prefix="/customers", tags=["customers"])
# api_router.include_router(raw_materials_route.router, prefix="/raw_materials", tags=["raw_materials"])
# api_router.include_router(inventory_route.router, prefix="/inventory", tags=["inventory"])
