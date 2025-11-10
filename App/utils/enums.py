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
    AJUSTE_POSITIVO = 'ajuste_positivo'
    AJUSTE_NEGATIVO = 'ajuste_negativo'
    MERMA = 'merma'
    DEVOLUCION_ENTRADA = 'devolucion_entrada' # devuelve proveddor a nosostros
    DEVOLUCION_SALIDA = 'devolucion_salida' # cliente nos devuelve
    TRANSFERENCIA_ENTRADA = 'transferencia_entrada'
    TRANSFERENCIA_SALIDA = 'transferencia_salida'


class MovementStatus (str, Enum):
    PENDIENTE = 'pendiente'
    COMPLETADO = 'completado'
    CANCELADO = 'cancelado'

# Unidades de medida
class UnitOfMeasure(Enum):
    KG = 'kg'
    L = 'l'
    UNIDAD = 'und'
    M = 'm'
    M2 = 'm2'
    M3 = 'm3'
    CAJA = 'caja'
    PAQUETE = 'paquete'
    
# Tipos de estado
class OrderStatus(Enum):
    PENDIENTE = 'pendiente'
    EN_PROCESO = 'en_proceso'
    COMPLETADO = 'completado'
    CANCELADO = 'cancelado'