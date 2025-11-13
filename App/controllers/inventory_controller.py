from decimal import Decimal
from operator import and_
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models.raw_material import RawMaterial
from app.models.inventory_model import Inventory
from app.models.movement_model import Movement
from app.utils.enums import MovementType
from fastapi import HTTPException


class InventoryController:
    def __init__(self, db: Session):
        self.db = db

    def get_or_create_inventory(self, material_id: int) -> Inventory:
        # Validar que el material existe
        material = self.db.query(RawMaterial).filter(
            RawMaterial.id == material_id).first()

        if not material:
            raise HTTPException(status_code=404, detail="Material not found")

        # Obtener o crear inventario
        inventory = self.db.query(Inventory).filter(
            Inventory.raw_material_id == material_id).first()

        if not inventory:
            inventory = Inventory(
                raw_material_id=material_id,
                quantity=Decimal('0.000'),
                location=None,
                warehouse=None
            )
        self.db.add(inventory)
        self.db.flush()

        return inventory

    """
    Registrar entrada de material
    """

    def register_entry(
        self,
        material_id: int,
        quantity: float,
        user_id: int,
        reference: Optional[str] = None,
        notes: Optional[str] = None,
        supplier_id: Optional[int] = None
    ) -> Movement:

        try:
            # verificar que la cantidad sea mayor a 0
            if quantity <= 0:
                raise HTTPException(
                    status_code=400, detail="Quantity must be greater than 0")

            # obtener o crear inventario
            inventory = self.get_or_create_inventory(material_id)

            # Guardar estado anterior
            quantity_before = inventory.quantity
            quantity_after = inventory.quantity + quantity

            # Crear movimiento de entrada
            movement = Movement(
                raw_material_id=material_id,
                user_id=user_id,
                type=MovementType.ENTRADA,
                quantity=quantity,
                quantity_before=quantity_before,
                quantity_after=quantity_after,
                reference=reference,
                notes=notes,
                supplier_id=supplier_id,
                customer_id=None
            )

            db.add(movement)
            db.flush()  # Para obtener el ID del movimiento

            # Actualizar inventario
            inventory.quantity += quantity
            inventory.last_movement_id = movement.id

            # Confirmar transaccion
            db.commit()
            db.refresh(movement)
            db.refresh(inventory)

            return movement

        except HTTPException:
            db.rollback()
            raise

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    """
    Registrar salida de material
    """

    def register_exit(
        self,
        material_id: int,
        quantity: float,
        reference: str,
        notes: str,
        user_id: int,
        customer_id: int
    ):
        try:

            # verificar que la cantidad sea mayor a 0
            if quantity <= 0:
                raise HTTPException(
                    status_code=400, detail="Quantity must be greater than 0")

            # Obtener inventario
            inventory = self.db.query(Inventory).filter(
                Inventory.raw_material_id == material_id).first()

            if not inventory:
                raise HTTPException(
                    status_code=404, detail="Stock not found")

            # verificar stock suficiente
            if inventory.quantity < quantity:
                raise HTTPException(status_code=400, detail="Not enough stock")

            # Guardar estado anterior
            quantity_before = inventory.quantity
            quantity_after = inventory.quantity - quantity

            # Crear movimiento de salida
            movement = Movement(
                raw_material_id=material_id,
                user_id=user_id,
                type=MovementType.SALIDA,
                quantity=quantity,
                quantity_before=quantity_before,
                quantity_after=quantity_after,
                reference=reference,
                notes=notes,
                supplier_id=None,
                customer_id=customer_id
            )

            db.add(movement)
            db.flush()  # Para obtener el ID del movimiento

            # Actualizar inventario
            inventory.quantity = quantity_after
            inventory.last_movement_id = movement.id

            # Confirmar transaccion
            db.commit()
            db.refresh(movement)
            db.refresh(inventory)

            return movement

        except HTTPException:
            db.rollback()
            raise

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    """
    Ajustar stock
    """
    def adjust_stock(
        db: Session,
        material_id: int,
        quantity: float,
        reference: str,
        notes: str,
        user_id: int,
        type: MovementType
    ) -> Movement:
        """
        Ajustar stock manualmente (invnetario fisico, correciones)

        Args:
            quantity: Puede ser positivo (aumentar) o negativo (disminuir)
            type: AJUSTE_POSITIVO o AJUSTE_NEGATIVO
        """

        try:
            # validar tipo de ajuste
            if type not in [MovementType.AJUSTE_POSITIVO, MovementType.AJUSTE_NEGATIVO]:
                raise HTTPException(
                    status_code=400, detail="Invalid adjustment type")

            # obtener o crear invnetario
            inventory = self.get_or_create_inventory(material_id)

            # Guardar estado anterior
            quantity_before = inventory.quantity
            quantity_after = inventory.quantity + quantity

            # validar que no quede negativo
            if quantity_after < 0:
                raise HTTPException(
                    status_code=400, detail="Stock cannot be negative")

            # Crear movimiento de ajuste
            movement = Movement(
                raw_material_id=material_id,
                user_id=user_id,
                type=type,
                quantity=quantity,
                quantity_before=quantity_before,
                quantity_after=quantity_after,
                reference=reference,
                notes=notes or "Ajuste manual",
                supplier_id=None,
                customer_id=None
            )

            db.add(movement)
            db.flush()  # Para obtener el ID del movimiento

            # Actualizar inventario
            inventory.quantity = quantity_after
            inventory.last_movement_id = movement.id

            # Confirmar transaccion
            db.commit()
            db.refresh(movement)
            db.refresh(inventory)

            return movement

        except HTTPException:
            db.rollback()
            raise

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    """
    Registrar merma
    """

    def register_merma(
        self,
        material_id: int,
        quantity: Decimal,
        user_id: int,
        reason: str,
        reference: Optional[str] = None
    ) -> Movement:
        """
        Registrar merma (pérdida, daño, vencimiento)
        """
        try:
            if quantity <= 0:
                raise HTTPException(
                    status_code=400, detail="Quantity must be greater than 0")

            inventory = self.db.query(Inventory).filter(
                Inventory.raw_material_id == material_id).first()

            if not inventory:
                raise HTTPException(status_code=404, detail="Stock not found")

            if inventory.quantity < quantity:
                raise HTTPException(status_code=400, detail="Not enough stock")

            # Guardar estado anterior
            quantity_before = inventory.quantity
            quantity_after = inventory.quantity - quantity

            movement = Movement(
                raw_material_id=material_id,
                user_id=user_id,
                type=MovementType.MERMA,
                quantity=quantity,
                quantity_before=quantity_before,
                quantity_after=quantity_after,
                reference=reference,
                notes=f"MERMA - Reason: {reason}",
                supplier_id=None,
                customer_id=None
            )

            db.add(movement)
            db.flush()  # Para obtener el ID del movimiento

            # Actualizar inventario
            inventory.quantity = quantity_after
            inventory.last_movement_id = movement.id

            # Confirmar transaccion
            db.commit()
            db.refresh(movement)
            db.refresh(inventory)

            return movement

        except HTTPException:
            db.rollback()
            raise

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    """
    Consultar stock actual
    """

    def get_stock(self, material_id: int) -> Optional[Inventory]:
        inventory = self.db.query(Inventory).filter(
            Inventory.raw_material_id == material_id).first()

        if not inventory:
            raise HTTPException(status_code=404, detail="Stock not found")

        return inventory

    """
    Obtener todo el inventario
    """

    def get_all_stock(
        self,
        skip: int = 0,
        limit: int = 100
    ) -> List[Inventory]:
        return self.db.query(Inventory).offset(skip).limit(limit).all()

    """
    Consultar movimientos
    """

    def get_movements(
        self,
        skip: int = 0,
        limit: int = 100
    ) -> List[Movement]:
        return self.db.query(Movement).offset(skip).limit(limit).all()

    """
    Consultar materiales con bajo stock
    """

    def get_low_stock_materials(
        self,
        skip: int = 0,
        limit: int = 100
    ) -> List[Inventory]:
        low_stock = self.db.query(Inventory).join(RawMaterial).filter(and_(
            Inventory.quantity <= RawMaterial.min_stock.min_stock,
            RawMaterial.is_active == True)).all()

        if not low_stock:
            raise HTTPException(status_code=404, detail="Low stock not found")

        return low_stock

    """
    Obtener materiales sin stock
    """

    def get_out_of_stock_materials(self) -> List[Inventory]:
        return self.db.query(Inventory).filter(Inventory.quantity == 0).all()

    """
    Calcular valor total del invnetario
    """

    def get_inventory_value(self) -> Decimal:
        total = db.query(func.sum(Inventory.quantity * RawMaterial.unit_price)).join(
            RawMaterial).filter(
            RawMaterial.is_active == True).scalar()

        return total or Decimal('0.00')

    """
    Cancelar movimmiento (reversa)
    """

    def cancel_movement(
        self,
        movement_id: int,
        user_id: int,
        reason: str
    ) -> Movement:
        """
        Cancelar un movimiento (crea un movimiento de reversa)
        IMPORTANTE: No elimina el movimiento original, lo marca como cancelado
        y crea un nuevo movimiento inverso
        """

        try:

            movement = self.db.query(Movement).filter(
                Movement.id == movement_id).first()

            if not movement:
                raise HTTPException(
                    status_code=404, detail="Movement not found")

            if movement.is_cacelled:
                raise HTTPException(
                    status_code=400, detail="Movement already cancelled")

            # Marcar movimiento como cancelado
            movement.is_cacelled = True
            movement.cancelled_at = func.now()
            movement.cancelled_by = user_id
            movement.cancellation_reason = reason

            # Obtener inventario actual
            inventory = self.db.query(Inventory).filter(
                Inventory.raw_material_id == movement.raw_material_id).first()

            if not inventory:
                raise HTTPException(status_code=404, detail="Stock not found")

            # Crear un NUEVO movimiento de reversa
            quantity_before = inventory.quantity 
            quantity_after = inventory.quantity - movement.quantity

            reverse_movement = Movement(
                raw_material_id=movement.raw_material_id,
                user_id=user_id,
                type=MovementType.AJUSTE_NEGATIVO if movement.quantity > 0 else MovementType.AJUSTE_POSITIVO,
                quantity=movement.quantity,
                quantity_before=quantity_before,
                quantity_after=quantity_after,
                reference=f"REVERSE-{movement.id}",
                notes=f"Reversa de movimiento {movement.id}",
                supplier_id=None,
                customer_id=None
            )

            # Guardar movimiento de reversa
            self.db.add(reverse_movement)
            self.db.flush()

            # Actualizar inventario
            inventory.quantity = quantity_after
            inventory.last_movement_id = reverse_movement.id

            # Confirmar transaccion
            self.db.commit()
            self.db.refresh(movement)
            self.db.refresh(inventory)

            return movement

        except HTTPException:
            self.db.rollback()
            raise

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
