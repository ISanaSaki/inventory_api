from sqlalchemy import Column, Integer, String, Text,Boolean
from app.core.database import Base

class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    contact = Column(String(100), nullable=True)
    address = Column(Text, nullable=True)
    is_deleted = Column(Boolean, default=False)