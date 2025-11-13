from decimal import Decimal
from typing import Optional
from pydantic import BaseModel
from pydantic import Field
from datetime import datetime


class InventoryBase(BaseModel):
    """Base model para inventario"""
    quantity: Decimal = Field(ge=0, description="Cantidad en stock")
    location: Optional[str] = Field(None, max_length=100)
    warehouse: Optional[str] = Field(None, max_length=100)


class InventoryResponse(InventoryBase):
    """Response de consulta de inventario   z"""
    id: int
    raw_material_id: int
    last_updated: datetime
    created_at: datetime

    # Información del material
    material_name: Optional[str] = None
    material_code: Optional[str] = None
    unit_of_measure: Optional[str] = None
    min_stock: Optional[Decimal] = None

    # Alertas
    is_low_stock: bool = False
    is_out_of_stock: bool = False

    class Config:
        from_attributes = True


class InventoryWithMaterial(InventoryResponse):
    """Response de consulta de inventario con material"""
    pass


class StockSummary(BaseModel):
    """Resumen de stock para dashboard"""
    total_materials: int
    materials_in_stock: int
    materials_low_stock: int
    materials_out_of_stock: int
    total_inventory_value: Decimal


class LowStockAlert(BaseModel):
    """Alerta de materiales cons stock bajo"""
    materia_id: int
    matrial_name: str
    material_code: str
    current_stock: Decimal
    min_stock: Decimal
    unit_of_measure: str
    difference: Decimal

    class Config:
        from_attributes = True
