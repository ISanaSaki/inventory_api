from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import HTTPException
from app.products.models import Product
from app.products.schemas import ProductCreate
from app.inventory.models import Inventory
from app.core.query_utils import apply_pagination,apply_sorting
from app.users.models import User
from app.audit.service import log_action
from fastapi.encoders import jsonable_encoder

def create_product(db: Session, data: ProductCreate, current_user: User):
    existing = db.query(Product).filter(
        Product.sku == data.sku,
        Product.is_deleted == False
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="SKU already exists")

    product = Product(**data.dict())
    db.add(product)
    db.commit()
    db.refresh(product)

    log_action(
    db=db,
    user_id=current_user.id,
    action="CREATE",
    entity="product",
    entity_id=product.id,
    new_data=jsonable_encoder(data.dict())
)

    return product

def get_products(
    db: Session,
    page: int,
    page_size: int,
    offset: int,
    sort_by: str | None,
    sort_order: str,
    category_id: int | None = None,
    name: str | None = None,
    search: str | None = None,
):
    query = db.query(Product).filter(Product.is_deleted == False)

    if category_id:
        query = query.filter(Product.category_id == category_id)

    if name:
        query = query.filter(Product.name.ilike(f"%{name}%"))

    if search:
        query = query.filter(
            Product.name.ilike(f"%{search}%")
        )

    total = query.count()

    query = apply_sorting(query, Product, sort_by, sort_order)

    query = apply_pagination(query, offset, page_size)

    items = query.all()

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": items,
    }

def get_product(db: Session, product_id: int):
    return db.query(Product).filter(
        Product.id == product_id,
        Product.is_deleted == False
    ).first()

def update_product(db, product_id: int, data, current_user):
    product = get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    payload = data.dict(exclude_unset=True)

    if not payload:
        return product

    old_data = jsonable_encoder({
        "name": product.name,
        "sku": product.sku,
        "price": getattr(product, "price", None),
        "description": product.description,
        "unit": product.unit,
        "min_quantity": product.min_quantity,
        "category_id": product.category_id,
    })

    if "sku" in payload and payload["sku"] != product.sku:
        existing = db.query(Product).filter(
            Product.sku == payload["sku"],
            Product.is_deleted == False
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="SKU already exists")

    for key, value in payload.items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)

    log_action(
        db=db,
        user_id=current_user.id,
        action="UPDATE",
        entity="product",
        entity_id=product.id,
        old_data=old_data,
        new_data=jsonable_encoder(payload),
    )

    return product

def delete_product(
    db: Session,
    product_id: int,
    current_user: User
):

    product = get_product(db, product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    inventory_exists = db.query(Inventory).filter(
        Inventory.product_id == product_id
    ).first()

    if inventory_exists:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete product with inventory transactions"
        )

    product.is_deleted = True
    db.commit()
    db.refresh(product)
    
    log_action(
    db=db,
    user_id=current_user.id,
    action="DELETE",
    entity="product",
    entity_id=product.id,
    old_data={"is_deleted": False},
    new_data={"is_deleted": True}
)

    return product
