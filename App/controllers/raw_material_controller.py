from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from app.models.raw_material_model import RawMaterial
from app.models.supplier_material_model import SupplierMaterial
from app.schemas.raw_material_schema import RawMaterialCreate, RawMaterialResponse, RawMaterialUpdate
from app.schemas.supplier_schema import SupplierMaterialCreate


class RawMaterialController:
    def __init__(self, db: Session):
        self.db = db

    @staticmethod
    def get_by_code(db: Session, code: str):
        return db.query(RawMaterial).filter(RawMaterial.code == code).first()

    @staticmethod
    def get_with_suppliers(db: Session, material_id: int) -> Optional[RawMaterial]:
        return db.query(RawMaterial).options(
            joinedload(RawMaterial.suppliers_associations)
        ).filter(RawMaterial.id == material_id).first()

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

    @staticmethod
    def list_multi(db: Session, skip: int = 0, limit: int = 100) -> list[RawMaterial]:
        return db.query(RawMaterial).offset(skip).limit(limit).all()

    @staticmethod
    def assign_supplier_to_material(
        db: Session,
        material_id: int,
        supplier_id: int,
        supplier_price: Decimal,
        is_preferred: bool = False,
        lead_time_days: int = 0,
        min_order_quantity: Decimal = Decimal('0.00'),
    ) -> SupplierMaterial:

        existing = db.query(SupplierMaterial).filter(
            SupplierMaterial.supplier_id == supplier_id,
            SupplierMaterial.material_id == material_id
        ).first()

        if existing:
            existing.supplier_price = supplier_price
            existing.is_preferred = is_preferred
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
                is_preferred=is_preferred,
                lead_time_days=lead_time_days,
                min_order_quantity=min_order_quantity
            )

            db.add(new_supplier_material)
            db.commit()
            db.refresh(new_supplier_material)

            return new_supplier_material

    @staticmethod
    def remove_supplier(db: Session, *, material_id: int, supplier_id: int) -> bool:
        # Desasgignar un proveedor de un material
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

    @staticmethod
    def create_raw_material(db: Session, raw_material: RawMaterialCreate) -> RawMaterialResponse:

        new_raw_material = RawMaterial(
            name=raw_material.name,
            code=raw_material.code,
            description=raw_material.description,
            unit_of_measure=raw_material.unit_of_measure,
            unit_price=raw_material.unit_price,
            min_stock=raw_material.min_stock,
            max_stock=raw_material.max_stock,
            reorder_point=raw_material.reorder_point,
            category=raw_material.category
        )

        db.add(new_raw_material)
        db.commit()
        db.refresh(new_raw_material)

        # si hay relaciones con proveedores, se manejan aparte
        return new_raw_material

    @staticmethod
    def update_material(db: Session, material_id: int, raw_material_update: RawMaterialUpdate) -> RawMaterial:
        raw_material = db.query(RawMaterial).filter(
            RawMaterial.id == material_id).first()

        if raw_material:
            raw_material.name = raw_material_update.name or raw_material.name
            raw_material.code = raw_material_update.code or raw_material.code
            raw_material.description = raw_material_update.description or raw_material.description
            raw_material.unit_of_measure = raw_material_update.unit_of_measure or raw_material.unit_of_measure
            raw_material.unit_price = raw_material_update.unit_price or raw_material.unit_price
            raw_material.min_stock = raw_material_update.min_stock or raw_material.min_stock
            raw_material.max_stock = raw_material_update.max_stock or raw_material.max_stock
            raw_material.reorder_point = raw_material_update.reorder_point or raw_material.reorder_point
            raw_material.category = raw_material_update.category or raw_material.category
            raw_material.updated_at = datetime.now() or raw_material.updated_at
            db.commit()
            db.refresh(raw_material)
            return raw_material
        return None

    def delete_raw_material(self, db: Session, *, material_id: int) -> bool:
        raw_material = db.query(RawMaterial).filter(
            RawMaterial.material_id == material_id).first()

        if raw_material:
            db.delete(raw_material)
            db.commit()
            return True
        return False

    @staticmethod
    def get_raw_material(db: Session, material_id: int) -> Optional[RawMaterial]:
        return db.query(RawMaterial).filter(RawMaterial.id == material_id).first()
