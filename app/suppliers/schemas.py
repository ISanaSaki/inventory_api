from pydantic import BaseModel
from typing import Optional,List

class SupplierCreate(BaseModel):
    name: str
    contact: Optional[str] = None
    address: Optional[str] = None

class SupplierOut(BaseModel):
    id: int
    name: str
    contact: Optional[str]
    address: Optional[str]

    class Config:
        from_attributes = True

class SupplierList(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[SupplierOut]