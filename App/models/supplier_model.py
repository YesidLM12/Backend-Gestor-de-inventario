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
    # supplier = relationship("Supplier", back_populates="materials")

    #======================================
    # Relaciones
    #======================================

    # materials = relationship("Material", back_populates="supplier")

    #======================================
    # Columnas
    #======================================
    
    tax_id = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    
