from fastapi import APIRouter, Depends, HTTPException,Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.products.schemas import ProductCreate, ProductOut,ProductList
from app.products.service import create_product, get_products, get_product, update_product, delete_product
from app.core.dependencies import require_role,pagination_params,sorting_params
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

@router.get("/", response_model=ProductList)
def list_products(
    db: Session = Depends(get_db),
    pagination: dict = Depends(pagination_params),
    sorting: dict = Depends(sorting_params),
    search: str | None = Query(None),
):
    return get_products(
        db=db,
        page=pagination["page"],
        page_size=pagination["page_size"],
        offset=pagination["offset"],
        sort_by=sorting["sort_by"],
        sort_order=sorting["sort_order"],
        search=search,
    )

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