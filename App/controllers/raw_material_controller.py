from decimal import Decimal
from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from app.models.raw_material_model import RawMaterial
from app.models.supplier_material_model import SupplierMaterial
from app.schemas.raw_material_schema import RawMaterialCreate, SupplierMaterialCreate


class RawMaterialController:
    def __init__(self, db: Session):
        self.db = db

    def get_by_code(self, db: Session, *, code: str):
        return db.query(RawMaterial).filter(RawMaterial.code == code).first()

    def get_with_suppliers(self, db: Session, *, material_id: int) -> Optional[RawMaterial]:
        return db.query(RawMaterial).options(
            joinedload(RawMaterial.supplier)
        ).filter(RawMaterial.material_id == material_id).first()

    def get_active(self, db: Session, *, skip: int = 0, limit: int = 100) -> list[RawMaterial]:
        return db.query(RawMaterial).filter(
            RawMaterial.is_active == True
        ).offset(skip).limit(limit).all()
    

    def get_by_category(self, db: Session, *, category: str) -> list[RawMaterial]:
        return db.query(RawMaterial).filter(
            RawMaterial.category == category
        ).all()


    def get_low_stock(self, db: Session, *, skip: int = 0, limit: int = 100) -> list[RawMaterial]:
        pass
    

    def list_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> list[RawMaterial]:
        return db.query(RawMaterial).filter(
            RawMaterial.is_active == True
        ).offset(skip).limit(limit).all()


    def assign_supplier(self,
     db: Session,
     *, material_id: int,
     supplier_id: int,
     supplier_price: Decimal,
     is_prefered: bool=False,
     lead_time_days: int = 0,
     min_order_quantity: Decimal = Decimal('0.00'),
    ) -> SupplierMaterial:

        existing = db.query(SupplierMaterial).filter(
            SupplierMaterial.supplier_id == supplier_id,
            SupplierMaterial.material_id == material_id
        ).first()

        if existing:
            existing.supplier_price = supplier_price
            existing.is_prefered = is_prefered
            existing.lead_time_days = lead_time_days
            existing.min_order_quantity = min_order_quantity
            db.commit()
            db.refresh(existing)
            return existing
        
        else:
            new_supplier_material = SupplierMaterial(
                material_id=material_id,
                supplier_id=supplier_id,
                supplier_price=supplier_price,
                is_prefered=is_prefered,
                lead_time_days=lead_time_days,
                min_order_quantity=min_order_quantity
            )

            db.add(new_supplier_material)
            db.commit()
            db.refresh(new_supplier_material)

            return new_supplier_material
    

    def remove_supplier(self, db: Session, *, material_id: int, supplier_id: int) -> bool:
        # Designar un proveedor de un material
        supplier_material = db.query(SupplierMaterial).filter(
            SupplierMaterial.supplier_id == supplier_id,
            SupplierMaterial.material_id == material_id
        ).first()

        if supplier_material:
            db.delete(supplier_material)
            db.commit()
            return True
        return False
    

    def get_supplier(self, db: Session, *, material_id: int) -> List[SupplierMaterial]:
        return db.query(SupplierMaterial).filter(
            SupplierMaterial.material_id == material_id
        ).all()
    

    def create_raw_material(self, db: Session, *, raw_material: RawMaterialCreate) -> RawMaterial:
        new_raw_material = RawMaterial(
            material_id=raw_material.material_id,
            supplier_id=raw_material.supplier_id,
            supplier_price=raw_material.supplier_price,
            is_prefered=raw_material.is_prefered,
            lead_time_days=raw_material.lead_time_days,
            min_order_quantity=raw_material.min_order_quantity
        )

        db.add(new_raw_material)
        db.commit()
        db.refresh(new_raw_material)

        return new_raw_material

    
    def update_raw_material(self, db: Session, *, material_id: int, raw_material: RawMaterialCreate) -> RawMaterial:
        raw_material = db.query(RawMaterial).filter(RawMaterial.material_id == material_id).first()

        if raw_material:
            raw_material.material_id = raw_material.material_id
            raw_material.supplier_id = raw_material.supplier_id
            raw_material.supplier_price = raw_material.supplier_price
            raw_material.is_prefered = raw_material.is_prefered
            raw_material.lead_time_days = raw_material.lead_time_days
            raw_material.min_order_quantity = raw_material.min_order_quantity
            db.commit()
            db.refresh(raw_material)
            return raw_material
        return None
    

    def delete_raw_material(self, db: Session, *, material_id: int) -> bool:
        raw_material = db.query(RawMaterial).filter(RawMaterial.material_id == material_id).first()

        if raw_material:
            db.delete(raw_material)
            db.commit()
            return True
        return False
    

    def get_raw_material(self, db: Session, *, material_id: int) -> Optional[RawMaterial]:
        return db.query(RawMaterial).filter(RawMaterial.material_id == material_id).first()