from app.db.session import Base
from sqlalchemy import Column, Integer, Numeric, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship

"""
    Tabla intermedia entre proveedor y material
"""


class SupplierMaterial(Base):
    __tablename__ = "supplier_material"

    # Clave primaria compuesta
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), primary_key=True)
    material_id = Column(Integer, ForeignKey(
        "raw_materials.id"), primary_key=True)

    # Información especifica de esta relación
    supplier_price = Column(Numeric(10, 2), nullable=False)
    is_preferred = Column(Boolean, nullable=False)
    lead_time_days = Column(Integer, default=0)
    min_order_quantity = Column(Numeric(10, 2), default=0)

    # Auditoria
    supplier = relationship(
        "Supplier", back_populates="materials_associations")
    material = relationship(
        "RawMaterial", back_populates="suppliers_associations")
