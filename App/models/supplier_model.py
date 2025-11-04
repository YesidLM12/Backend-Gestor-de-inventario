from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

class Supplier(Base):

    #======================================
    # Tabla
    #======================================
    __tablename__ = "suppliers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    contact_name = Column(String, unique=True, index=True)
    phone = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"))

    #======================================
    # Control
    #======================================
    
    tax_id = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    materials_associations = relationship("SupplierMaterial", back_populates="supplier", cascade="all, delete-orphan")

    @property
    def raw_materials(self):
        return [material.material for material in self.materials_associations]

    
