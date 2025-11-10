from enum import Enum
from tkinter import NO
from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal
from app.utils.enums import MovementType
from pydantic import field_validator
from datetime import datetime


class MovementBase(BaseModel):
    """Base para Movement"""
    raw_material_id: int
    type: MovementType
    quantity: Decimal = Field(
        description="Cantidad (positiva para entradas, negativa para salidas)")
    reference: Optional[str] = Field(
        None, max_length=100, description="Número de orden, factura, etc.")
    notes: Optional[str] = None
    supplier_id: Optional[int] = None
    customer_id: Optional[int] = None


class MovementCreate(MovementBase):
    """Crear nuevo movimiento"""

    @field_validator("quantity")
    def validate_quantity(cls, v, values):
        """Validar que la cantidad sea coherente con el tipo de movimiento"""
        if 'type' in values:
            movement_type = values['type']

            # Tipos que requieren cantidad positiva
            entrada_types = [
                MovementType.ENTRADA,
                MovementType.AJUSTE_POSITIVO,
                MovementType.DEVOLUCION_ENTRADA,
                MovementType.TRANSFERENCIA_ENTRADA
            ]

            # Tipos que requieren cantidad negativa
            salida_types = [
                MovementType.SALIDA,
                MovementType.AJUSTE_NEGATIVO,
                MovementType.DEVOLUCION_SALIDA,
                MovementType.TRANSFERENCIA_SALIDA
            ]

            if movement_type in entrada_types and v <= 0:
                raise ValueError(
                    f'Para {movement_type.name} la cantidad debe ser positiva')

            if movement_type in salida_types and v >= 0:
                return -abs(v)

        return v


class MovementUpdate(MovementBase):
    """Actualizar movimiento (Solo notas, no cantidad ni tipo)"""
    notes: Optional[str] = None
    reference: Optional[str] = None


class MovementResponse(MovementBase):
    """Response de movimiento"""
    id: int
    user_id: Optional[int]
    quantity_before: Decimal
    quantity_after: Decimal
    created_at: datetime
    is_cacelled: bool = False

    # información adicional
    user_name: Optional[str] = None
    material_name: Optional[str] = None
    material_code: Optional[str] = None

    class Config:
        from_attributes = True


class MovementWithDetails(MovementResponse):
    """Movimiento con todos los detalles"""
    supplier_name: Optional[str] = None
    customer_name: Optional[str] = None
    cancelled_at: Optional[datetime] = None
    cancelled_by: Optional[int] = None
    cancellation_reason: Optional[str] = None


class MovementFilter(BaseModel):
    """Filtros para movimiento"""
    raw_material_id: Optional[int] = None
    type: Optional[MovementType] = None
    user_id: Optional[int] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    reference: Optional[str] = None
    supplier_id: Optional[int] = None
    customer_id: Optional[int] = None
    skip: int = Field(0, ge=0)
    limit: int = Field(10, ge=1, le=100)
    

class CancelMovement(BaseModel):
    """Cancelar movimiento"""
    reason: str = Field(min_length=1, max_length=500, description="Razon de cancelacion")