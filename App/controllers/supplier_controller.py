
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from app.db.session import Base
from app.models.supplier_model import Supplier
from app.models.raw_material_model import RawMaterial
from app.schemas.supplier_schema import SupplierCreate

class SupplierController:

    def __init__(self, db: Session):
        self.db = db

    def get_active(self):
        return self.db.query(Supplier).filter(Supplier.is_active == True).all()

    
    def get_with_materials(self, supplier_id: int):
        return (
            self.db.query(Supplier)
            .options(joinedload(Supplier.materials))
            .filter(Supplier.id == supplier_id)
            .first()
        )

    
    def search_by_name(self, name: str):
        return self.db.query(Supplier).filter(Supplier.name.contains(name)).all()


    def create_supplier(self, supplier_data: SupplierCreate):

        supplier = Supplier(
            name=supplier_data.name,
            contact_name=supplier_data.contact_name,
            phone=supplier_data.phone,
            email=supplier_data.email,
            tax_id=supplier_data.tax_id,
            is_active=supplier_data.is_active
        )

        if supplier_data.materials:
            materials = [RawMaterial(**material.dict()) for material in supplier_data.materials]

            supplier.materials = materials
        
        self.db.add(supplier)
        self.db.commit()
        self.db.refresh(supplier)

        return supplier


    def update_supplier(self, supplier_id: int, supplier_data: SupplierCreate):
        supplier = self.db.query(Supplier).filter(Supplier.id == supplier_id).first()

        if not supplier:
            raise HTTPException(status_code=404, detail="Supplier not found")

        supplier.name = supplier_data.name
        supplier.contact_name = supplier_data.contact_name
        supplier.phone = supplier_data.phone
        supplier.email = supplier_data.email
        supplier.tax_id = supplier_data.tax_id
        supplier.is_active = supplier_data.is_active

        self.db.add(supplier)
        self.db.commit()
        self.db.refresh(supplier)

        return supplier
    
    def delete_supplier(self, supplier_id: int):
        supplier = self.db.query(Supplier).filter(Supplier.id == supplier_id).first()

        if not supplier:
            raise HTTPException(status_code=404, detail="Supplier not found")

        self.db.delete(supplier)
        self.db.commit()

        return supplier
    

    def get_all_suppliers(self):
        return self.db.query(Supplier).all()
    
