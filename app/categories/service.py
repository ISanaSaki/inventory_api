from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.categories.models import Category
from app.categories.schemas import CategoryCreate
from app.products.models import Product
from sqlalchemy import or_
from app.core.query_utils import apply_pagination,apply_sorting

def create_category(db: Session, data: CategoryCreate):
    existing = db.query(Category).filter(
        Category.name == data.name,
        Category.is_deleted == False
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Category already exists")

    category = Category(
        name=data.name,
        description=data.description
    )

    db.add(category)
    db.commit()
    db.refresh(category)
    return category

def get_categories(
    db: Session,
    page: int,
    page_size: int,
    offset: int,
    sort_by: str | None,
    sort_order: str,
    search: str | None = None,
):
    query = db.query(Category).filter(Category.is_deleted == False)

    if search:
        query = query.filter(
            or_(
                Category.name.ilike(f"%{search}%"),
                Category.description.ilike(f"%{search}%"),
            )
        )

    total = query.count()

    query = apply_sorting(query, Category, sort_by, sort_order)

    query = apply_pagination(query, offset, page_size)

    items = query.all()

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": items,
    }

def get_category(db: Session, category_id: int):
    return db.query(Category).filter(
        Category.id == category_id,
        Category.is_deleted==False
        ).first()

def update_category(db: Session, category_id: int, data: CategoryCreate):
    category = get_category(db, category_id)

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    if data.name != category.name:
        existing = db.query(Category).filter(
            Category.name == data.name,
            Category.is_deleted == False
        ).first()

        if existing:
            raise HTTPException(status_code=400, detail="Category already exists")

    category.name = data.name
    category.description = data.description

    db.commit()
    db.refresh(category)
    return category

def delete_category(db: Session, category_id: int):
    category = get_category(db, category_id)

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    product_exists = db.query(Product).filter(
        Product.category_id == category_id,
        Product.is_deleted == False
    ).first()

    if product_exists:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete category with active products"
        )

    category.is_deleted = True
    db.commit()
    db.refresh(category)

    return category