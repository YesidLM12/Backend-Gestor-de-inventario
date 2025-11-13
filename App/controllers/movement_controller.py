
from decimal import Decimal
from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import date, datetime
from app.models.movement import Movement
from app.utils.enums import MovementType


class MovementController:
    """
    CRUD para consultar movimientos de inventario

    NOTA: Este CRUD solo CONSULTA, no crea movimientos
    """

    def __init__(self, db: Session):
        self.db = db

    """
    Obtener movimientos por id
    """

    def get_movement_by_id(self, movement_id: int) -> Movement:
        movement = self.db.query(Movement).filter(
            Movement.id == movement_id).first()
        if not movement:
            raise HTTPException(status_code=404, detail="Movement not found")
        return movement

    """
    Obtener historial de un material
    """

    def get_by_material_id(
        self,
        material_id: int,
        skip: int = 0,
        limit: int = 100,
        include_cancelled: bool = False
    ) -> List[Movement]:

        query = self.db.query(Movement).filter(
            Movement.material_id == material_id)

        # Por defecto, excluir cancelados
        if not include_cancelled:
            query = query.filter(Movement.cancelled == False)

        # Ordenar por fecha descendentemente
        query = query.order_by(Movement.created_at.desc())

        # Aplicar paginación
        movements = query.offset(skip).limit(limit).all()

        return movements

    """
    Obtener movimientos por usuario
    """

    def get_by_user(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        include_cancelled: bool = False,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> List[Movement]:

        query = self.db.query(Movement).filter(
            Movement.user_id == user_id)

        if not include_cancelled:
            query = query.filter(Movement.cancelled == False)

        if date_from:
            query = query.filter(Movement.created_at >= date_from)

        if date_to:
            query = query.filter(Movement.created_at <= date_to)

        query = query.order_by(Movement.created_at.desc())

        movements = query.offset(skip).limit(limit).all()

        return movements

    """
    Filtrar solo ENTRADAS, o solo SALIDAS, o solo MERMAS
    """

    def get_by_type(
        self,
        movement_type: MovementType,
        skip: int = 0,
        limit: int = 100,
        include_cancelled: bool = False,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> List[Movement]:

        query = self.db.query(Movement).filter(
            Movement.type == movement_type)

        if not include_cancelled:
            query = query.filter(Movement.cancelled == False)

        if date_from:
            query = query.filter(Movement.created_at >= date_from)

        if date_to:
            query = query.filter(Movement.created_at <= date_to)

        query = query.order_by(Movement.created_at.desc())

        movements = query.offset(skip).limit(limit).all()

        return movements

    """
    Obtener movimientos por fecha
    """

    def get_by_date_range(
        self,
        date_from: date,
        date_to: date,
        material_id: Optional[int] = None,
        movement_type: Optional[MovementType] = None,
        skip: int = 0,
        limit: int = 100,
        include_cancelled: bool = False
    ) -> List[Movement]:
        query = self.db.query(Movement).filter(
            Movement.created_at >= date_from,
            Movement.created_at <= date_to
        )

        if material_id:
            query = query.filter(Movement.material_id == material_id)

        if movement_type:
            query = query.filter(Movement.type == movement_type)

        if not include_cancelled:
            query = query.filter(Movement.cancelled == False)

        query = query.order_by(Movement.created_at.desc())

        movements = query.offset(skip).limit(limit).all()

        return movements

    """
    Busqueda avanzada
    """

    def get_with_filters(
        self,
        material_id: Optional[int] = None,
        user_id: Optional[int] = None,
        movement_type: Optional[MovementType] = None,
        skip: int = 0,
        limit: int = 100,
        include_cancelled: bool = False,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        reference: Optional[str] = None,
        supplier_id: Optional[int] = None,
        customer_id: Optional[int] = None,
    ) -> List[Movement]:
        query = self.db.query(Movement)

        if material_id:
            query = query.filter(Movement.material_id == material_id)

        if user_id:
            query = query.filter(Movement.user_id == user_id)

        if movement_type:
            query = query.filter(Movement.type == movement_type)

        if reference:
            query = query.filter(Movement.reference == reference)

        if supplier_id:
            query = query.filter(Movement.supplier_id == supplier_id)

        if customer_id:
            query = query.filter(Movement.customer_id == customer_id)

        if not include_cancelled:
            query = query.filter(Movement.cancelled == False)

        if date_from:
            query = query.filter(Movement.created_at >= date_from)

        if date_to:
            query = query.filter(Movement.created_at <= date_to)

        query = query.order_by(Movement.created_at.desc())

        movements = query.offset(skip).limit(limit).all()

        return movements

    """
    Obtener resumen de movimiento de un material
    """

    def get_summary(
        self,
        material_id: int,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> MovementSummary:
        query = self.db.query(Movement).filter(
            Movement.material_id == material_id,
            Movement.is_cancelled == False
        )

        if date_from:
            query = query.filter(Movement.created_at >= date_from)

        if date_to:
            query = query.filter(Movement.created_at <= date_to)

        # Obtener todos los movimientos
        movements = query.all()

        # Inicializar contadores
        summary = {
            'material_id': material_id,
            'period': {
                'from': date_from.isoformat() if date_from else None,
                'to': date_to.isoformat() if date_to else None
            },
            'total_movements': len(movements),
            'entradas': {
                'cantidad': Decimal('0.000'),
                'movimientos': 0
            },
            'salidas': {
                'cantidad': Decimal('0.000'),
                'movimientos': 0
            },
            'ajustes_positivos': {
                'cantidad': Decimal('0.000'),
                'movimientos': 0
            },
            'ajustes_negativos': {
                'cantidad': Decimal('0.000'),
                'movimientos': 0
            },
            'mermas': {
                'cantidad': Decimal('0.000'),
                'movimientos': 0
            },
            'balance': Decimal('0.000'),
            'stock_inicial': None,
            'stock_final': None
        }

        # Procesar cada movimiento
        for mov in movements:
            # Guardar stock inicial
            if summary['stock_inicial'] is None:
                summary['stock_inicial'] = mov.initial_stock

            # Actualizar stoc final
            summary['stock_final'] = mov.final_stock

            # Clasificar por tipo
            if mov.type == MovementType.ENTRADA:
                summary['entradas']['cantidad'] += mov.quantity
                summary['entradas']['movimientos'] += 1

            elif mov.type == MovementType.SALIDA:
                summary['salidas']['cantidad'] += mov.quantity
                summary['salidas']['movimientos'] += 1

            elif mov.type == MovementType.AJUSTE_POSITIVO:
                summary['ajustes_positivos']['cantidad'] += mov.quantity
                summary['ajustes_positivos']['movimientos'] += 1

            elif mov.type == MovementType.AJUSTE_NEGATIVO:
                summary['ajustes_negativos']['cantidad'] += mov.quantity
                summary['ajustes_negativos']['movimientos'] += 1

            elif mov.type == MovementType.MERMA:
                summary['mermas']['cantidad'] += mov.quantity
                summary['mermas']['movimientos'] += 1

            # Calcular balance
            summary['balance'] = (
                summary['entradas']['cantidad'] +
                summary['ajustes_positivos']['cantidad'] -
                summary['salidas']['cantidad'] -
                summary['ajustes_negativos']['cantidad'] -
                summary['mermas']['cantidad']
            )

        return summary
