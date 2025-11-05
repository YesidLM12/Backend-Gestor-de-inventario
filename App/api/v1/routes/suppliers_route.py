from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.permissions import require_role
from app.schemas.supplier_schema import SupplierCreate
from app.utils.enums import UserRole
from app.api.deps import get_db
from app.controllers.supplier_controller import SupplierController
from app.api.deps import get_current_manager
from app.models.user_model import User

router = APIRouter(prefix="/suppliers", tags=["Suppliers"])

@router.post("/")
async def add_supplier(supplier_data: SupplierCreate,
 db: Session = Depends(get_db),
 current_user: User = Depends(get_current_manager)
):
    return SupplierController(db).create_supplier(supplier_data)



@router.get("/")
async def get_all_suppliers(db: Session = Depends(get_db)):
    return SupplierController(db).get_all_suppliers()


@router.get("/{supplier_id}")
async def get_supplier_by_id(supplier_id: int, db: Session = Depends(get_db)):
    return SupplierController(db).get_supplier_by_id(supplier_id)


@router.put("/{supplier_id}")
async def update_supplier(supplier_id: int, supplier_data: SupplierCreate, db: Session = Depends(get_db),
 current_user: User = Depends(get_current_manager)):
    return SupplierController(db).update_supplier(supplier_id, supplier_data)


@router.delete("/{supplier_id}")
async def delete_supplier(supplier_id: int, db: Session = Depends(get_db),
 current_user: User = Depends(get_current_manager)):
    return SupplierController(db).delete_supplier(supplier_id)


@router.get("/{supplier_id}/materials")
async def get_supplier_materials(supplier_id: int, db: Session = Depends(get_db),
 current_user: User = Depends(get_current_manager)):
    return SupplierController(db).get_with_materials(supplier_id)



