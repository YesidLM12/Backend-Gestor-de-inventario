from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

from pydantic.v1 import validator

class SupplierBase(BaseModel):
    name: str
    contact_name: Optional[str]
    phone: str
    email: EmailStr
    tax_id: str

    @validator('phone')
    def phone_validator(cls, v):

        patron = r'^\+?1?\d{9,15}$'

        if not re.match(patron, v):
            raise ValueError('El número de teléfono no es válido')
        return v

class SupplierCreate(SupplierBase):
    pass

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
