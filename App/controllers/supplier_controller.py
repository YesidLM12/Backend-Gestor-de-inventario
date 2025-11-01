
from sqlalchemy.orm import Session
from app.controllers.base_controller import BaseController
from app.db.session import Base


class SupplierController(BaseController):

    def create(self, db: Session, obj_in: Base):
        return super().create(db, obj_in)
    
    def update(self, db: Session, id: int, obj_in: Base):
        return super().update(db, id, obj_in)
    
    def delete(self, db: Session, id: int):
        return super().delete(db, id)
    
    def get_all(self, db: Session):
        return super().get_all(db)
    
    def get_by_id(self, db: Session, id: int):
        return super().get_by_id(db, id)
    
    def get_multi(self, db: Session, skip: int = 0, limit: int = 100):
        return super().get_multi(db, skip, limit)
    
    def get_active(self, db: Session):
        return db.query(self.model).filter(self.model.is_active == True).all()
    
    
    def get_with_materials(self, db: Session, id: int):
        return db.query(self.model).filter(self.model.id == id).first()
    
    def search_by_name(self, db: Session, name: str):
        return db.query(self.model).filter(self.model.name.contains(name)).all()
    

    
