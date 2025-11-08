
from sqlalchemy import Column, ForeignKey, Integer, Numeric, String, DateTime, func
from sqlalchemy.orm import relationship

class Inventory(Base):
    __tablename__ = "inventory"
    id = Column(Integer, primary_key=True, index=True)
    raw_material_id = Column(Integer, ForeignKey("raw_materials.id", ondelete="CASCADE"), nullable=False)
    quantity = Column(Numeric(12,3), nullable=False, default=0.00)
    location = Column(String(100), nullable=False)
    warehouse = Column(String(100), nullable=False)
    last_movement_id = Column(Integer, ForeignKey("movements.id"), nullable=True)
    last_update = Column(DateTime(timezone=True), server_default=func.now(),onupdate=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relaciones
    raw_material = relationship(
        "RawMaterial",
        back_populates="inventory",
        uselist=False # One-to- ON: devuelve objeto, no lista
    )

    last_movement = relationship(
        "Movement",
        back_populates="inventory",
        uselist=False
    )

    __table_args__ = (
        Index('idx_inventory_material', raw_material_id),
        Index('idx_inventory_quantity', quantity)
    )

    def __repr__ (self):
        return f'I<nventory(material_id={self.raw_material_id}, quantity={self.quantity})>'
    