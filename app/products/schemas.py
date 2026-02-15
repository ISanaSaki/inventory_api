from pydantic import BaseModel
from typing import Optional,List

class ProductCreate(BaseModel):
    name: str
    category_id: int
    sku: str
    description: Optional[str] = None
    unit: str
    min_quantity: float = 0

class ProductOut(BaseModel):
    id: int
    name: str
    category_id: int
    sku: str
    description: Optional[str]
    unit: str
    min_quantity: float

    class Config:
        from_attributes = True

class ProductList(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[ProductOut]