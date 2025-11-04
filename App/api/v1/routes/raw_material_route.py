from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.controllers.raw_material_controller import RawMaterialController
from app.core.dependencies import get_db
from app.core.permissions import require_role
from app.schemas.raw_material_schema import AssignSupplierSchema, RawMaterialResponse, RawMaterialCreate, RawMaterialUpdate
from app.models.user_model import User
from app.utils.enums import UserRole

router = APIRouter(prefix="/raw_materials", tags=["raw_materials"])


@router.get('/', response_model=list[RawMaterialResponse])
def list_raw_materials(skip: int = 0,
                       limit: int = 100,
                       db: Session = Depends(get_db)):
    materials = RawMaterialController.list_mult(skip, limit, db)
    return materials


@router.get('/active', response_model=list[RawMaterialResponse])
def list_active_raw_materials(skip: int = 0,
                              limit: int = 100,
                              db: Session = Depends(get_db)):
    materials = RawMaterialController.get_active(skip, limit, db)
    return materials


@router.get('/{material_id}', response_model=RawMaterialResponse)
def get_raw_material(material_id: int,
                     db: Session = Depends(get_db)):
    material = RawMaterialController.get_raw_material(material_id, db)
    return material


@require_role(UserRole.ADMIN or UserRole.MANAGER)
@router.post('/', response_model=RawMaterialResponse, status_code=status.HTTP_201_CREATED)
def create_raw_material(raw_material: RawMaterialCreate,
                        db: Session = Depends(get_db),
                        ):

    existing = RawMaterialController.get_by_code(db, code=raw_material.code)

    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Raw material with this code already exists")

    material = RawMaterialController.create_raw_material(db, raw_material)
    return material


@require_role(UserRole.ADMIN or UserRole.MANAGER)
@router.put('/{material_id}', response_model=RawMaterialResponse)
def update_raw_material(material_id: int,
                        raw_material: RawMaterialUpdate,
                        db: Session = Depends(get_db),
                        ):
    material = RawMaterialController.get_raw_material(material_id, db)

    if not material:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Raw material not found"
        )

    if raw_material.code and raw_material.code != material.code:
        existing = RawMaterialController.get_by_code(
            db, code=raw_material.code)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Raw material with this code already exists"
            )

        material = RawMaterialController.update_raw_material(
            material_id, raw_material, db)
        return material


@require_role(UserRole.ADMIN)
@router.delete('/{material_id}', response_model=RawMaterialResponse)
def delete_raw_material(material_id: int,
                        db: Session = Depends(get_db),
                        ):

    material = RawMaterialController.get_raw_material(material_id, db)
    if not material:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Raw material not found"
        )

    material.is_active = False
    db.commit()
    return None


@require_role(UserRole.ADMIN or UserRole.MANAGER)
@router.post('/{material_id}/suppliers', status_code=status.HTTP_201_CREATED)
def assign_supplier_to_material(
    material_id: int,
    supplier_data: AssignSupplierSchema,
    db: Session = Depends(get_db),
):
    material = RawMaterialController.get_raw_material(material_id, db)

    if not material:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Raw material not found"
        )

    supplier_material = RawMaterialController.assign_supplier_to_material(
        db,
        material_id=material_id,
        supplier_id=supplier_data.supplier_id,
        supplier_price=supplier_data.supplier_price,
        is_preferred=supplier_data.is_preferred,
        lead_time_days=supplier_data.lead_time_days,
        min_order_quantity=supplier_data.min_order_quantity,
    )

    return {'message': 'Supplier assigned to material successfully', 'data': supplier_material}


@require_role(UserRole.ADMIN or UserRole.MANAGER)
@router.delete('/{material_id}/suppliers/{supplier_id}', status_code=status.HTTP_204_NO_CONTENT)
def remove_supplier_from_material(
    material_id: int,
    supplier_id: int,
    db: Session = Depends(get_db),
):
    success = RawMaterialController.remove_supplier_from_material(
        db,
        material_id=material_id,
        supplier_id=supplier_id,
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Raw material not found"
        )

    return None


@require_role(UserRole.ADMIN or UserRole.MANAGER)
@router.get('/{material_id}/suppliers', response_model=list[RawMaterialResponse])
def get_suppliers_by_material_id(
    material_id: int,
    db: Session = Depends(get_db),
):
    material = RawMaterialController.get_raw_material(material_id, db)

    if not material:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Raw material not found"
        )
    
    suppliers = RawMaterialController.get_with_suppliers(material_id, db)
    
    return suppliers
