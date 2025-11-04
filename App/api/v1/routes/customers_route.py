from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controllers.customer_controller import CustomerController
from app.core.dependencies import get_db
from app.core.permissions import require_role
from app.schemas.customer_schema import CustomerResponse, CustomerCreate, CustomerUpdate
from app.schemas.user_schema import UserRole

router = APIRouter(prefix="/customers", tags=["customers"])


@router.get('/', response_model=list[CustomerResponse])
def list_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    customers = CustomerController(db).get_multi(skip, limit)
    return customers


@router.get('/active', response_model=list[CustomerResponse])
def list_active_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    customers = CustomerController(
        db).get_active_customers(skip=skip, limit=limit)
    return customers


@require_role(UserRole.MANAGER or UserRole.ADMIN)
@router.get('with-debt', response_model=list[CustomerResponse])
def list_customers_with_debt(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    customers = CustomerController(
        db).get_customers_with_debt(skip=skip, limit=limit)
    return customers


@router.get('/{customer_id}', response_model=CustomerResponse)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = CustomerController(db).get_customer_by_id(customer_id)

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )
    return customer


@require_role(UserRole.MANAGER or UserRole.ADMIN)
@router.post('/', response_model=CustomerResponse)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    constumer = CustomerController(db).create_customer(customer)
    return constumer


@require_role(UserRole.MANAGER or UserRole.ADMIN)
@router.put('/{customer_id}', response_model=CustomerResponse)
def update_customer(customer_id: int, customer: CustomerUpdate, db: Session = Depends(get_db)):
    constumer = CustomerController(db).update_customer(customer_id, customer)

    if not constumer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )
    return constumer


@require_role(UserRole.ADMIN)
@router.delete('/{customer_id}', response_model=CustomerResponse)
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = CustomerController(db).get_customer_by_id(customer_id)

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    customer.is_active = False
    db.commit()

    return None
