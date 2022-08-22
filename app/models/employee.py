from app.db.base_class import Base

from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, DateTime, Boolean

class Employee(Base):
    id = Column(Integer, primary_key=True)
    email = Column(String(255), nullable=True)
    name = Column(String(255), nullable=False)
    cellphone = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default = func.now())
    rol = Column(Integer, nullable=False)
    is_superuser = Column(Boolean, default=False)
    hashed_password = Column(String(255), nullable=False)
    