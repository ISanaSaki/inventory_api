from sqlalchemy import Column, Integer, String, ForeignKey, Text, Float, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"))
    sku = Column(String(50), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    unit = Column(String(20), nullable=False)  
    min_quantity = Column(Float, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    category = relationship("Category", backref="products")