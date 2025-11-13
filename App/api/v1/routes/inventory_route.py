from decimal import Decimal
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.api.deps import get_current_user
from app.core.dependencies import get_db
from app.controllers.inventory_controller import InventoryController
from app.controllers.movement_controller import MovementController
from app.schemas.movement_schema import CancelMovement, MovementCreate, MovementResponse, MovementWithDetails
from app.models.user_model import User
from app.core.dependencies import get_current_admin_or_manager
from app.utils.enums import UserRole
router = APIRouter(prefix="/inventory", tags=["inventory"])

"""
Rgistrar Movimientos
"""

# Registrar entrada


@router.post('/entry', response_model=MovementCreate, status_code=status.HTTP_201_CREATED, summary="Registrar entrada de material")
async def register_entry(
    material_id: int,
    quantity: Decimal = Query(..., ge=1, description="Cantidad de material"),
    reference: Optional[str] = None,
    notes: Optional[str] = None,
    supplier_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Require: OPERATOR o superior

    - Valida que el material existe
    - Crea registro en movements
    - Actualiza stock en inventory
    - Todo es una transacción atómica
    """

    # Validar permisos
    if current_user.role == UserRole.VIEWER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    movement = InventoryController.register_entry(
        db=db,
        material_id=material_id,
        quantity=quantity,
        user_id=current_user.id,
        reference=reference,
        notes=notes,
        supplier_id=supplier_id
    )

    return movement


# Registrar salida
@router.post('/exit', response_model=MovementResponse, status_code=status.HTTP_201_CREATED, summary="Registrar salida de material")
async def register_exit(
    material_id: int,
    quantity: Decimal = Query(..., ge=0, description="Cantidad de material"),
    reference: Optional[str] = None,
    notes: Optional[str] = None,
    customer_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Requiere: OPERATOR o superior

    - valida stock disponible
    - crea registro en movements
    - Disminuye stock de inventario
    - Error si stock no es suficiente
    """

    if current_user.role == UserRole.VIEWER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    movement = InventoryController.register_exit(
        db=db,
        material_id=material_id,
        quantity=quantity,
        user_id=current_user.id,
        reference=reference,
        notes=notes,
        customer_id=customer_id
    )

    return movement


# Ajustar stock
@router.post('/adjustment', response_model=MovementResponse, status_code=status.HTTP_201_CREATED, summary="Ajustar stock")
async def adjust_stock(
    material_id: int,
    quantity: Decimal = Query(..., ge=0, description="Cantidad de material"),
    adjustment_type: MovementType = Query(..., description="Tipo de ajuste"),
    reference: Optional[str] = None,
    notes: Optional[str] = None,
    user_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Requiere: MANAGER o ADMIN

    - Se usa cuando hay diferencias entre inventario físico y sistema
    - Requiere especificar razón obligatoriamente
    - Puede ser positivo o negativo
    """

    # Validar tipo de auste
    if adjustment_type not in [MovementType.AJUSTE_POSITIVO, MovementType.AJUSTE_NEGATIVO]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Tipo de ajuste no válido")

    movement = InventoryController.adjust_stock(
        db=db,
        material_id=material_id,
        quantity=quantity,
        adjustment_type=adjustment_type,
        reference=reference,
        notes=notes,
        user_id=current_user.id
    )

    return movement


# Registrar merma
@router.post('/merma', response_model=MovementResponse, status_code=status.HTTP_201_CREATED, summary="Registrar merma")
async def register_merma(
    material_id: int,
    quantity: Decimal = Query(..., ge=0, description="Cantidad de material"),
    reason: Optional[str] = None,
    reference: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Requiere: OPERATOR o superior

    - Se usa para pérdidas no vendibles
    - Disminuye el stock
    - Requiere especificar razón
    """

    if current_user.role == UserRole.VIEWER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    movement = InventoryController.register_merma(
        db=db,
        material_id=material_id,
        quantity=quantity,
        user_id=current_user.id,
        reason=reason,
        reference=reference,
    )

    return movement


"""
Consultar STOCK
"""

# Consultar todo el inventario


@router.get('/', response_model=list[InventoryResponse], summary="Consultar stock")
async def get_all_inventory(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtener todo el invnetario paginado

    Todos los usuaarios pueden consultar
    """
    inventory = InventoryController.get_all_stock(
        db=db, skip=skip, limit=limit)
    return inventory


# Consultar stock de un material
@router.get('/{material_id}', response_model=InventoryResponse, summary="Consultar stock de un material")
async def get_inventory_by_material_id(
    material_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtener el stock de un material específico

    Devuelve:
    - Cantidad en stock
    - Ubicación
    -Última actualización
    """
    inventory = InventoryController.get_stock(
        db=db, material_id=material_id)
    return inventory


# Obtener materailes con stock <= stock minimo
@router.get('/alerts/low-stock', response_model=list[InventoryResponse], summary="Consultar stock de materiales con stock <= stock minimo")
async def get_low_stock(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtener todos los materiales con stock <= stock minimo

    Útil para alertas y reposición
    """
    inventory = InventoryController.get_low_stock_materials(
        db=db)
    return inventory


# Obtener materiales con stock 0
@router.get('/alerts/out-of-stock', response_model=list[InventoryResponse], summary="Consultar stock de materiales con stock 0")
async def get_stock_0(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtener todos los materiales con stock 0

    CRITICO: Materiales que no se pueden vender
    """
    out_of_stock = InventoryController.get_stock_out_of_stock_materials(
        db=db)
    return out_of_stock


# Obtener valor total del inventario
@router.get('/value/total', response_model=Decimal, summary="Consultar valor total del inventario")
async def get_inventory_value(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtener el valor total del inventario
    Requiere: MANAGER o ADMIN
    Fómula: SUM(quantity * unit_price)
    """
    total_value = InventoryController.get_inventory_value(db=db)
    return {
        "total_value": total_value,
        'currency': 'USD',
        'calculated_at': datetime.now()
    }


"""
Historial de movimientos
"""

# Obtener historial de movimientos
@router.get('/movements', response_model=list[MovementResponse], summary="Consultar historial de movimientos")
async def get_movements(
    material_id: Optional[int] = None,
    user_id: Optional[int] = None,
    movement_type: Optional[MovementType] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    reference: Optional[str] = None,
    supplier_id: Optional[int] = None,
    customer_id: Optional[int] = None,
    include_cancelled: Optional[bool] = False,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtener el historial de movimientos con multiples filtros
    Requiere: MANAGER o ADMIN
    """
    movements = MovementController.get_with_filters(
        db=db,
        material_id=material_id,
        user_id=user_id,
        movement_type=movement_type,
        date_from=date_from,
        date_to=date_to,
        reference=reference,
        supplier_id=supplier_id,
        customer_id=customer_id,
        include_cancelled=include_cancelled,
        skip=skip,
        limit=limit
    )
    return movements


# Obtener información de un movimiento específico
@router.get('/movements/{movement_id}', response_model=MovementWithDetails, summary="Consultar información de un movimiento específico")
async def get_movement_detail(
    movement_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtener información de un movimiento específico
    
    Incluye:
    - Datos de movimiento
    - Usuario que lo realizó
    - Material afectado
    - Stock antes/despues
    - Proveedor/cliente
    """
    movement = MovementController.get_by_id(db=db, movement_id=movement_id)
    return movement


# Obtener resumen estadistico de movimientos de un material
@router.get('/movements/summary/{material_id}', summary="Consultar resumen estadistico de movimientos de un material")
async def get_movement_summary(
    material_id: int,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtener resumen estadistico de movimientos de un material
    Devuelve:
    - Total de entradas
    - Total de salidas
    - Total de ajustes positivos
    - Total de ajustes negativos
    - Total de mermas
    - Balance
    - Stock inicial
    - Stock final
    """
    summary = MovementController.get_summary(db=db, material_id=material_id, date_from=date_from, date_to=date_to)
    return summary


"""
Administración
"""

# Cancelar movimiento
@router.put('/movements/{movement_id}/cancel', response_model=MovementResponse, summary="Cancelar movimiento")
async def cancel_movement(
    movement_id: int,
    cancel_data: CancelMovement,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_or_manager)
):
    """
    Cancelar un movimiento
    Requiere: MANAGER o ADMIN

    IMPORTANTE: 
    - No elimina el movimiento original
    - Lo marca como cancelado
    - Crea un nuevo movimiento inverso para revertir el movimiento original
    - Requiere especificar razón de cancelación

    Casos de uso:
    - Error en el registro
    - Devolución de mercancia
    - Corrección de datos
    """
    reversal_movement = MovementController.cancel_movement(
        db=db,
        movement_id=movement_id,
        user_id=current_user.id,
        reason=cancel_data.reason
    )
    return reversal_movement
