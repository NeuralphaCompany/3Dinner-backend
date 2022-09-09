from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .category import Category

class Producto(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(300), nullable=False)
    short_description = Column(String(150), nullable=True)
    price = Column(Integer, nullable=False)
    image = Column(String(1000), nullable=True)
    image_galery = Column(JSON, nullable=True)
    ingredients = Column(JSON, nullable=True)
    BaseIVA = Column(Integer, nullable=True, default=0)
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship("Category", back_populates="products")
