class InsufficientStockException(Exception):
    """Excepción lanzada cuando no hay stock suficiente para realizar una operación."""
    def __init__(self, producto_id, cantidad_disponioble):
        super().__init__(f"El producto {producto_id} no tiene stock suficiente. Stock disponible: {cantidad_disponioble}")

class InvalidMovementException(Exception):
    """Excepción lanzada cuando se intenta realizar un movimiento con datos inválidos."""
    def __init__(self, mensaje):
        super().__init__(mensaje)

class DuplicateRecordException(Exception):
    """Excepción lanzada cuando se intenta crear un registro duplicado."""
    def __init__(self, mensaje):
        super().__init__(mensaje)

class PermissionDeniedException(Exception):
    """Excepción lanzada cuando se intenta acceder a una operación sin permisos."""
    def __init__(self, mensaje):
        super().__init__(mensaje)