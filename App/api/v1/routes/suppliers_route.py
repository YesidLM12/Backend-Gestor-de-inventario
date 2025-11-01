from fastapi import Router, Depends
from app.controllers.supplier_controller import SupplierController
from app.api.v1.dependencies import get_current_user
from app.schemas.supplier import SupplierResponse
from app.core.permissions import require_role
from app.utils.enums import UserRole

router = Router()

@require_role(UserRole.ADMIN | UserRole.MANAGER)
@router.post("/", response_model=SupplierResponse)
async def create_supplier(supplier: SupplierCreate, current_user: User = Depends(get_current_user)):
    return SupplierController.create(current_user.db, supplier)

@require_role(UserRole.ADMIN | UserRole.MANAGER)
@router.put("/{supplier_id}", response_model=SupplierResponse)
async def update_supplier(supplier_id: int, supplier: SupplierUpdate, current_user: User = Depends(get_current_user)):
    return SupplierController.update(current_user.db, supplier_id, supplier)

@require_role(UserRole.ADMIN)
@router.delete("/{supplier_id}")
async def delete_supplier(supplier_id: int, current_user: User = Depends(get_current_user)):
    return SupplierController.delete(current_user.db, supplier_id)

@router.get("/", response_model=list[SupplierResponse])
async def get_all_suppliers(current_user: User = Depends(get_current_user)):
    return SupplierController.get_all(current_user.db)

@router.get("/supplier/{supplier_id}", response_model=SupplierResponse)
async def get_supplier_by_id(supplier_id: int, current_user: User = Depends(get_current_user)):
    return SupplierController.get_by_id(current_user.db, supplier_id)

@router.get("/multi", response_model=list[SupplierResponse])
async def get_multi_suppliers(skip: int = 0, limit: int = 100, current_user: User = Depends(get_current_user)):
    return SupplierController.get_multi(current_user.db, skip, limit)

@router.get("/name/{name}", response_model=SupplierResponse)
async def get_supplier_by_name(name: str, current_user: User = Depends(get_current_user)):
    return SupplierController.get_by_name(current_user.db, name)


@router.get("/active", response_model=list[SupplierResponse])
async def get_active_suppliers(current_user: User = Depends(get_current_user)):
    return SupplierController.get_active(current_user.db)

@router.get("/{supplier_id}/materials", response_model=list[SupplierResponse])
async def get_supplier_with_materials(supplier_id: int, current_user: User = Depends(get_current_user)):
    return SupplierController.get_with_materials(current_user.db, supplier_id)

@router.get("/search/{name}", response_model=list[SupplierResponse])
async def search_supplier_by_name(name: str, current_user: User = Depends(get_current_user)):
    return SupplierController.search_by_name(current_user.db, name)
