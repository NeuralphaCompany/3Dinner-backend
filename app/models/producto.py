from sqlalchemy import Column, Integer, String

from app.db.base_class import Base

class Producto(Base):
    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), nullable=False)