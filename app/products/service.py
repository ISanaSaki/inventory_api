from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.products.models import Product
from app.products.schemas import ProductCreate
from app.inventory.models import Inventory

def create_product(db: Session, data: ProductCreate):
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
    return product

def get_products(db: Session, category_id: int = None, name: str = None):
    query = db.query(Product).filter(Product.is_deleted == False)

    if category_id:
        query = query.filter(Product.category_id == category_id)

    if name:
        query = query.filter(Product.name.ilike(f"%{name}%"))

    return query.all()

def get_product(db: Session, product_id: int):
    return db.query(Product).filter(
        Product.id == product_id,
        Product.is_deleted == False
    ).first()

def update_product(db: Session, product_id: int, data: ProductCreate):
    product = get_product(db, product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if data.sku != product.sku:
        existing = db.query(Product).filter(
            Product.sku == data.sku,
            Product.is_deleted == False
        ).first()

        if existing:
            raise HTTPException(status_code=400, detail="SKU already exists")

    for key, value in data.dict().items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)
    return product

def delete_product(db: Session, product_id: int):
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

    return product