from pydantic import BaseModel, validator,Field
from typing import Optional,List
from datetime import datetime
from app.common.enums import ChangeType
from enum import Enum

class ChangeType(str, Enum):
    IN = "IN"
    OUT = "OUT"

class InventoryCreate(BaseModel):
    product_id: int
    change_type: ChangeType
    quantity: float
    supplier_id: Optional[int] = None
    description: Optional[str] = None
    user_id: int
    
    @validator('change_type', pre=True)
    def validate_change_type(cls, v):
        if isinstance(v, str):
            v = v.upper()
            if v not in ['IN', 'OUT']:
                raise ValueError('change_type must be IN or OUT')
            return ChangeType(v)
        return v

class InventoryOut(BaseModel):
    id: int
    product_id: int
    change_type: str
    quantity: int
    user_id: int
    supplier_id: Optional[int] = None
    description: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class InventoryList(BaseModel):
    total: int
    page: int = Field(ge=1)
    page_size: int = Field(ge=1, le=100)
    items: List[InventoryOut]