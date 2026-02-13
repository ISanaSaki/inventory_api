from sqlalchemy.orm import Session
from app.categories.models import Category
from app.categories.schemas import CategoryCreate

def create_category(db: Session, category: CategoryCreate):
    existing = db.query(Category).filter(Category.name == category.name).first()
    if existing:
        raise ValueError("Category already exists")
    cat = Category(name=category.name, description=category.description)
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat

def get_categories(db: Session):
    return db.query(Category).all()

def get_category(db: Session, category_id: int):
    return db.query(Category).filter(Category.id == category_id).first()

def update_category(db: Session, category_id: int, data: CategoryCreate):
    cat = get_category(db, category_id)
    if not cat:
        return None
    cat.name = data.name
    cat.description = data.description
    db.commit()
    db.refresh(cat)
    return cat

def delete_category(db: Session, category_id: int):
    cat = get_category(db, category_id)
    if not cat:
        return None
    # TODO: بررسی محصول مرتبط → بعداً
    db.delete(cat)
    db.commit()
    return cat