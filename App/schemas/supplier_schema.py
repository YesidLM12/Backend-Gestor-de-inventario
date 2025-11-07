from decimal import Decimal
from typing import List, Optional, TYPE_CHECKING
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from datetime import datetime

from pydantic.v1 import validator

if TYPE_CHECKING:
    from app.schemas.raw_material_schema import RawMaterialResponse

class SupplierBase(BaseModel):
    name: str
    contact_name: Optional[str]
    phone: str
    email: EmailStr
    tax_id: str
    is_active: bool
    # materials = List[materials]

    @validator('phone')
    def phone_validator(cls, v):

        patron = r'^\+?1?\d{9,15}$'

        if not re.match(patron, v):
            raise ValueError('El número de teléfono no es válido')
        return v

    class Config:
        orm_mode = True


class SupplierCreate(SupplierBase):
    materials: List['RawMaterialResponse'] = None
    is_active: bool = True


class SupplierUpdate(SupplierBase):
    pass


class SupplierResponse(BaseModel):
    id: int
    name: str
    contact_name: Optional[str]
    phone: str
    email: EmailStr
    tax_id: str
    is_active: bool
    created_at: datetime
    supplier_materials: List['RawMaterialResponse'] = []

    model_config = ConfigDict(from_attributes = True)


class SupplierMaterialBase(BaseModel):
    supplier_id: int
    supplier_price: Decimal = Field(gt=0, description="Precio del proveedor")
    is_preferred: bool = False
    lead_time_days: int = Field(gt=0, description="Tiempo de entrega")
    min_order_quantity: Decimal = Field(gt=0)


class SupplierMaterialCreate(SupplierMaterialBase):
    pass


class SupplierMaterialResponse(SupplierMaterialBase):
    supplier: 'SupplierResponse'
    material_id: int
    supplier_price: Decimal = Field(gt=0)
    is_preferred: bool
    lead_time_days: Optional[int] = 0
    min_order_quantity: Optional[Decimal] = 0
    last_purchase_date: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.now)

    

    # Incluir datos del supplier
    supplier_name: Optional[str] = None

    class Config:
        orm_mode = True

from app.schemas.raw_material_schema import RawMaterialResponse 
SupplierResponse.model_rebuild()
SupplierMaterialResponse.model_rebuild()