from sqlalchemy import Column, Integer, String, Enum as SQLAEnum, Boolean
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.utils.enums import UserRole


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(SQLAEnum(UserRole), default=UserRole.VIEWER,
                  nullable=False, index=True)
    is_active = Column(Boolean, default=True, nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)

    movements = relationship(
        'Movement', back_populates='user', foreign_keys='Movement.user_id')
    cancelled_movements = relationship(
        'Movement', back_populates='cancelled_by_user', foreign_keys='Movement.cancelled_by_user_id')

from app.models.movement_model import Movement
