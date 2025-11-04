
from sqlalchemy.orm import Session
from sqlalchemy import DECIMAL
from app.schemas.customer_schema import CustomerCreate, CustomerUpdate
from app.models.customer_model import Customer


class CustomerController:
    def __init__(self, db: Session):
        self.db = db


    def create_customer(self, customer: CustomerCreate):
        customer = Customer(**customer.model_dump())
        self.db.add(customer)
        self.db.commit()
        self.db.refresh(customer)
        return customer


    def get_all_customers(self):
        return self.db.query(Customer).all()
    

    def get_multi(self, skip: int = 0, limit: int = 100):
        return self.db.query(Customer).offset(skip).limit(limit).all()


    def get_active_customers(self):
        return self.db.query(Customer).filter(Customer.is_active == True).all()


    def get_customer_by_id(self, customer_id: int):
        return self.db.query(Customer).filter(Customer.id == customer_id).first()
    

    def get_customers_with_debt(self):
        return self.db.query(Customer).filter(Customer.cuerrent_balance > 0).all()

    def update_customer(self, customer_id: int, customer: CustomerUpdate):
        customer = self.db.query(Customer).filter(
            Customer.id == customer_id).first()
        customer.name = customer.name
        customer.contact_name = customer.contact_name
        customer.phone = customer.phone
        customer.email = customer.email
        customer.tax_id = customer.tax_id
        customer.discount_percentage = customer.discount_percentage
        customer.credit_limit = customer.credit_limit
        self.db.commit()
        return customer


    def delete_customer(self, customer_id: int):
        customer = self.db.query(Customer).filter(
            Customer.id == customer_id).first()
        self.db.delete(customer)
        self.db.commit()
        return customer

    def get_by_credit_limit(self, credit_limit: DECIMAL):
        return self.db.query(Customer).filter(Customer.credit_limit == credit_limit).all()

    def update_balance(self, customer_id: int, balance: DECIMAL):
        customer = self.db.query(Customer).filter(
            Customer.id == customer_id).first()

        if customer:
            customer.cuerrent_balance = balance
            self.db.commit()

        return customer
    

    def can_purchase(self, customer_id: int, amount: DECIMAL):
        customer = self.db.query(Customer).filter(
            Customer.id == customer_id).first()
        

        if customer:
            return customer.cuerrent_balance >= customer.credit_limit
        
        return False

