from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.products.schemas import ProductCreate, ProductOut
from app.products.service import create_product, get_products, get_product, update_product, delete_product
from app.core.dependencies import require_role
from app.common.enums import Role

router = APIRouter(
    prefix="/products",
    tags=["Products"],
    dependencies=[
        Depends(require_role([Role.ADMIN]))
    ]
)

@router.post("/", response_model=ProductOut)
def create_prod(data: ProductCreate, db: Session = Depends(get_db)):
    try:
        return create_product(db, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[ProductOut])
def list_products(category_id: int = None, name: str = None, db: Session = Depends(get_db)):
    return get_products(db, category_id, name)

@router.get("/{product_id}", response_model=ProductOut)
def retrieve_product(product_id: int, db: Session = Depends(get_db)):
    prod = get_product(db, product_id)
    if not prod:
        raise HTTPException(status_code=404, detail="Product not found")
    return prod

@router.put("/{product_id}", response_model=ProductOut)
def update_prod(product_id: int, data: ProductCreate, db: Session = Depends(get_db)):
    updated = update_product(db, product_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated

@router.delete("/{product_id}", response_model=ProductOut)
def delete_prod(product_id: int, db: Session = Depends(get_db)):
    deleted = delete_product(db, product_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Product not found")
    return deleted