from abc import ABC
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.db.session import Base

class BaseController(ABC):
    def get_all(self, db: Session):
        return db.query(self.model).all()
    
    def get_by_id(self, db: Session, id: int):
        return db.query(self.model).filter(self.model.id == id).first()
    
    def create(self, db: Session, obj_in: Base):
        db.add(obj_in)
        db.commit()
        db.refresh(obj_in)
        return obj_in   
    
    def update(self, db: Session, id: int, obj_in: Base):
        obj = db.query(self.model).filter(self.model.id == id).first()
        if not obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Object not found')
        obj = obj_in
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj
    
    def delete(self, db: Session, id: int):
        obj = db.query(self.model).filter(self.model.id == id).first()
        if not obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Object not found')
        db.delete(obj)
        db.commit()
        return obj
    
    def get_multi(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(self.model).offset(skip).limit(limit).all()