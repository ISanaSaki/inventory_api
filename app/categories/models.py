from sqlalchemy import Column, Integer, String, Text,Boolean
from app.core.database import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    is_deleted = Column(Boolean, default=False)