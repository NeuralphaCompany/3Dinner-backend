from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, JSON, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User

class Venta(Base):
    id = Column(Integer, primary_key=True)
    productos = Column(JSON, nullable=False)
    adiciones = Column(JSON, nullable=True)
    cantidadxadiciones = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="ventas")