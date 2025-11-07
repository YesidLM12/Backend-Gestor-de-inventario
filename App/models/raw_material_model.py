from sqlalchemy import Column, Enum, Integer, Numeric, String, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.utils.enums import UnitOfMeasure


class RawMaterial(Base):
    __tablename__ = "raw_materials"

    # Identificación
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), unique=True, index=True)
    code = Column(String(50), unique=True,nullable=False, index=True)
    description = Column(String, nullable=True)

    # Medidas y precioo
    unit_of_measure = Column(Enum(UnitOfMeasure), nullable=False)
    unit_price = Column(Numeric(10,2), default=0.00)

    # Control de stock
    min_stock = Column(Numeric(10,2), default=0.00)
    max_stock = Column(Numeric(10,2), default=0.00)
    reorder_point = Column(Numeric(10,2), nullable=True)

    # Categorización
    category = Column(String(100), nullable=True, index=True)
    
    # Control
    is_active = Column(Boolean, default=True, index=True)

    # Auditoria
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Realciones
    suppliers_associations = relationship("SupplierMaterial", back_populates="material", cascade="all, delete-orphan")

    @property
    def suppliers(self):
        return self.suppliers_associations
        
    @property
    def preferred_supplier(self):
        return [supplier.supplier for supplier in self.suppliers_associations if supplier.is_preferred]