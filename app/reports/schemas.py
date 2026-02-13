from pydantic import BaseModel

class CurrentStockOut(BaseModel):
    product_id: int
    product_name: str
    current_stock: float