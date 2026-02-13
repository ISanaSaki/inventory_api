from sqlalchemy.orm import Session
from app.products.models import Product
from app.products.schemas import ProductCreate

def create_product(db: Session, data: ProductCreate):
    if db.query(Product).filter(Product.sku == data.sku).first():
        raise ValueError("SKU already exists")
    product = Product(**data.dict())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def get_products(db: Session, category_id: int = None, name: str = None):
    query = db.query(Product)
    if category_id:
        query = query.filter(Product.category_id == category_id)
    if name:
        query = query.filter(Product.name.ilike(f"%{name}%"))
    return query.all()

def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

def update_product(db: Session, product_id: int, data: ProductCreate):
    product = get_product(db, product_id)
    if not product:
        return None
    for key, value in data.dict().items():
        setattr(product, key, value)
    db.commit()
    db.refresh(product)
    return product

def delete_product(db: Session, product_id: int):
    product = get_product(db, product_id)
    if not product:
        return None
    # TODO: بررسی تراکنش‌های موجود در inventory → بعداً
    db.delete(product)
    db.commit()
    return product