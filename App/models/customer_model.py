

from sqlalchemy import DECIMAL, Column, ForeignKey, Boolean, DateTime, String,Integer
from sqlalchemy.orm import relationship
from app.db.session import Base
from datetime import datetime


class Customer(Base):
    __tablename__ = "customers"

    # ======================================
    # Columnas
    # ======================================
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    contact_name = Column(String, unique=True, index=True)
    phone = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    address = Column(String, unique=True, index=True)
    tax_id = Column(String, unique=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))

    # ======================================
    # Campos especificos de customer
    # ======================================
    discount_percentage = Column(DECIMAL, default=0)
    credit_limit = Column(DECIMAL, default=0)
    current_balance = Column(DECIMAL, default=0)

    # ======================================
    # Control
    # ======================================
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # ======================================
    # Relaciones
    # ======================================
    # orders = relationship("Order", back_populates="customer")
