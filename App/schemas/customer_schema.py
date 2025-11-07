
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, EmailStr
from datetime import datetime

class CustomerBase(BaseModel):
    name: str
    contact_name: Optional[str]
    phone: str
    email: EmailStr
    tax_id: str
    discount_percentage: Decimal = Decimal("0.00")
    credit_limit: Decimal = Decimal("0.00")


class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(CustomerBase):
    pass

class CustomerResponse(CustomerBase):
    id: int
    current_balance: Decimal
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
