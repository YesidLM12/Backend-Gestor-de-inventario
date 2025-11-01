from enum import Enum

# Roles del sistema
class UserRole(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    OPERATOR = "operator"
    VIEWER = "viewer"

# Tipos de movimiento
class MovementType(Enum):
    ENTRADA = 'entrada'
    SALIDA = 'salida'
    AJUSTE = 'ajuste'
    MERMA = 'merma'

# Unidades de medida
class UnitOfMeasure(Enum):
    KG = 'kg'
    L = 'l'
    UNIDAD = 'und'
    M = 'm'
    M2 = 'm2'
    M3 = 'm3'
    
# Tipos de estado
class OrderStatus(Enum):
    PENDIENTE = 'pendiente'
    EN_PROCESO = 'en_proceso'
    COMPLETADO = 'completado'
    CANCELADO = 'cancelado'