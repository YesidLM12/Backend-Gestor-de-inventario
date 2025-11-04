
from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel, Field, validator

from app.utils.enums import UnitOfMeasure


class SupplierMaterialBase(BaseModel):
    supplier_id: int
    supplier_price: Decimal = Field(gt=0,description="Precio del proveedor")
    is_preferred: bool = False
    lead_time_days: int = Field(gt=0,description="Tiempo de entrega")
    min_order_quantity: Decimal = Field(gt=0)


class SupplierMaterialCreate(SupplierMaterialBase):
    pass


class SupplierMaterialResponse(SupplierMaterialBase):
    raw_material_id: int
    last_purchase_date: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.now)
    
    # Incluir datos del supplier
    supplier_name: Optional[str] = None

    class Config:
        orm_mode = True


class RawMaterialBase(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    code: str = Field(min_length=1, max_length=50)
    description: Optional[str] = None
    unit_of_measure: UnitOfMeasure
    unit_price: Decimal = Field(gt=0, default=Decimal("0.00"))
    min_stock: Decimal = Field(gt=0, default=Decimal("0.00"))
    max_stock: Optional[Decimal] = Field(gt=0, default=Decimal("0.00"))
    reorder_point: Optional[Decimal] = Field(gt=0, default=None)
    category_id: Optional[str] = Field(max_length=100, default=None)


class RawMaterialCreate(RawMaterialBase):
    supplier_ids: Optional[List[int]] = []

    @validator('max_stock')
    def validate_max_stock(cls, v, values):
        if v is not None and 'min_stock' in values:
            if v < values['min_stock']:
                raise ValueError('max_stock debe ser mayor o igual a min_stock')
        return v


class RawMaterialUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    code: Optional[str] = Field(None, min_length=1, max_length=50)
    description: Optional[str] = None
    unit_of_measure: Optional[UnitOfMeasure] = None
    unit_price: Optional[Decimal] = Field(None, ge=0)
    min_stock: Optional[Decimal] = Field(None, ge=0)
    max_stock: Optional[Decimal] = Field(None, ge=0)
    reorder_point: Optional[Decimal] = Field(None, ge=0)
    category: Optional[str] = Field(None, max_length=100)
    is_active: Optional[bool] = None


class RawMaterialResponse(RawMaterialBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    # Stock actual (cuando lo tengamos implementado)
    current_stock: Optional[Decimal] = None
    
    # Lista de proveedores (nested)
    suppliers: Optional[List[dict]] = []
    
    class Config:
        from_attributes = True


class AssignSupplierSchema(BaseModel):
    supplier_id: int
    supplier_price: Decimal = Field(gt=0)
    is_preferred: bool = False
    lead_time_days: int = Field(ge=0, default=0)
    min_order_quantity: Decimal = Field(ge=0, default=Decimal("0.00"))