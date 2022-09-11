from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func

from sqlalchemy.orm import relationship

from app.services.db.base_class import Base

if TYPE_CHECKING:
    from .venta import Venta

class User(Base):
    id = Column(Integer, primary_key=True)
    email = Column(String(255), nullable=True)
    name = Column(String(255), nullable=False)
    cellphone = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default = func.now())
    ventas = relationship("Venta", back_populates="user")