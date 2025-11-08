
from typing import Text
from sqlalchemy import Column, ForeignKey, Index, Integer, Numeric, String, DateTime, Enum, func
from sqlalchemy.orm import relationship

from app.utils.enums import MovementType


class Movement(Base):
    __tablename__ = "movements"
    id = Column(Integer, primary_key=True, index=True)
    raw_material_id = Column(Integer, ForeignKey(
        'raw_materials.id', ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey(
        'users.id', ondelete="CASCADE"), nullable=False)
    movement_type = Column(Enum(MovementType), nullable=False, index=True)
    quantity = Column(Numeric(12, 3), nullable=False)
    quantity_before = Column(Numeric(12, 3), nullable=False)
    quantity_after = Column(Numeric(12, 3), nullable=False)
    reference = Column(String(100), nullable=False, index=True)
    notes = Column(String(255), nullable=True)

    # RElación con documentos externos
    order_id = Column(Integer, ForeignKey('orders.id', ondelete="SET NULL"), nullable=True, nullable=True)
    supplier_id = Column(Integer, ForeignKey('suppliers.id', ondelete="SET NULL"), nullable=True, nullable=True)
    customer_id = Column(Integer, ForeignKey('customers.id', ondelete="SET NULL"), nullable=True, nullable=True)

    # Auditoria temporal
    created_at = Column(DateTime(timezone=True),
                        server_default=func.now(), index=True)

    # Para cancelaciones
    is_cancelled = Column(Integer, default=0)
    cancelled_at = Column(DateTime(timezone=True), nullable=True)
    cancelled_by_user_id = Column(Integer, ForeignKey(
        'users.id', ondelete="SET NULL"), nullable=True)
    cancellation_reason = Column(Text(255), nullable=True)

    # relaciones
    raw_material = relationship("RawMaterial", back_populates="movements")
    user = relationship("User", back_populates="movements")

    supplier = relationship("Supplier")
    customer = relationship("Customer")

    cancelled_by_user = relationship(
        "User", back_populates="cancelled_movements")

    __table_args__ = (
        Index('idx_movement_material_date', 'raw_material_id', 'created_at'),
        Index('idx_movemente_type_date', 'movement_type', 'created_at'),
        Index('idx_movement_user_date', 'user_id', 'created_at'),
        Index('idx_movement_reference', 'reference'),
    )

    def __repr__(self):
        return f"<Movement(id={self.id}, raw_material_id={self.raw_material_id}, user_id={self.user_id}, movement_type={self.movement_type}, quantity={self.quantity})>"
