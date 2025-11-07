
from datetime import datetime
from decimal import Decimal
from typing import List, Optional, TYPE_CHECKING
from pydantic import BaseModel, ConfigDict, Field, validator

from app.utils.enums import UnitOfMeasure

if TYPE_CHECKING:
    from app.schemas.supplier_schema import SupplierMaterialResponse


class RawMaterialBase(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    code: str = Field(min_length=1, max_length=50)
    description: Optional[str] = None
    unit_of_measure: UnitOfMeasure
    unit_price: Decimal = Field(gt=0, default=Decimal("0.00"))
    min_stock: Decimal = Field(gt=0, default=Decimal("0.00"))
    max_stock: Optional[Decimal] = Field(gt=0, default=Decimal("0.00"))
    reorder_point: Optional[Decimal] = Field(gt=0, default=None)
    category: Optional[str] = Field(max_length=100, default=None)


class RawMaterialCreate(RawMaterialBase):
    supplier_ids: Optional[List[int]] = []
    supplier_price: Optional[Decimal] = None
    is_preferred: Optional[bool] = False
    lead_time_days: Optional[int] = None
    min_order_quantity: Optional[Decimal] = None

    @validator('max_stock')
    def validate_max_stock(cls, v, values):
        if v is not None and 'min_stock' in values:
            if v < values['min_stock']:
                raise ValueError(
                    'max_stock debe ser mayor o igual a min_stock')
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

class SupplierInfoInMaterial(BaseModel):
    supplier_id: int
    material_id: int
    supplier_price: Decimal
    is_preferred: bool
    lead_time_days: Optional[int] = 0
    min_order_quantity: Optional[Decimal] = 0

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class RawMaterialResponse(RawMaterialBase):
    id: int
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    code: Optional[str] = Field(None, min_length=1, max_length=50)
    unit_of_measure: UnitOfMeasure
    unit_price: Decimal = Field(gt=0, default=Decimal("0.00"))
    category: Optional[str] = Field(max_length=100, default=None)
    is_active: bool
    created_at: datetime

    # Stock actual (cuando lo tengamos implementado)
    current_stock: Optional[Decimal] = None

    # Lista de proveedores (nested)
    suppliers_associations: List[SupplierInfoInMaterial] = []

    class Config:
        orm_mode = True




class AssignSupplierSchema(BaseModel):
    supplier_id: int
    supplier_price: Decimal = Field(gt=0)
    is_preferred: bool = False
    lead_time_days: int = Field(ge=0, default=0)
    min_order_quantity: Decimal = Field(ge=0, default=Decimal("0.00"))


from app.schemas.supplier_schema import SupplierMaterialResponse
RawMaterialResponse.model_rebuild()