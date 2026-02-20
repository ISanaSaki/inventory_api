from pydantic import BaseModel,Field
from typing import Optional,List
from decimal import Decimal

class ProductCreate(BaseModel):
    name: str
    category_id: int
    sku: str
    description: Optional[str] = None
    unit: str
    min_quantity: float = 0
    price: Decimal = Field(..., gt=0)

class ProductOut(BaseModel):
    id: int
    name: str
    category_id: int
    sku: str
    description: Optional[str]
    unit: str
    min_quantity: float
    price: Decimal 

    class Config:
        from_attributes = True

class ProductList(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[ProductOut]


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    category_id: Optional[int] = None
    sku: Optional[str] = None
    description: Optional[str] = None
    unit: Optional[str] = None
    min_quantity: Optional[int] = Field(default=None, ge=0)
    price: Optional[float] = Field(default=None, ge=0)