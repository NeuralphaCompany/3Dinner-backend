from typing import TYPE_CHECKING
from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.orm import relationship

from app.services.db.base_class import Base

if TYPE_CHECKING:
    from .producto import Producto

class Category(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    image = Column(String(1000), nullable=True)
    products = relationship("Producto", back_populates="category")
