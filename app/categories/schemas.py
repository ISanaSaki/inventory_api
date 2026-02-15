from pydantic import BaseModel
from typing import Optional,List

class CategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryOut(BaseModel):
    id: int
    name: str
    description: Optional[str]

    class Config:
        from_attributes = True

class CategoryList(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[CategoryOut]