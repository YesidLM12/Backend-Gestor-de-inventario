from app.api.v1.routes import auth_route, users_route, suppliers_route, customers_route, raw_material_route, inventory_route
from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(auth_route.router)
api_router.include_router(users_route.router)
api_router.include_router(suppliers_route.router)
api_router.include_router(customers_route.router)   
api_router.include_router(raw_material_route.router)
api_router.include_router(inventory_route.router)
