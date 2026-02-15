from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.suppliers.models import Supplier
from app.suppliers.schemas import SupplierCreate
from sqlalchemy import or_
from app.core.query_utils import apply_pagination,apply_sorting

def create_supplier(db: Session, data: SupplierCreate):
    existing = db.query(Supplier).filter(
        Supplier.name == data.name,
        Supplier.is_deleted == False
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Supplier already exists")

    supplier = Supplier(**data.dict())
    db.add(supplier)
    db.commit()
    db.refresh(supplier)
    return supplier


def get_suppliers(
    db: Session,
    page: int,
    page_size: int,
    offset: int,
    sort_by: str | None,
    sort_order: str,
    search: str | None = None,
):
    query = db.query(Supplier).filter(Supplier.is_deleted == False)

    if search:
        query = query.filter(
            or_(
                Supplier.name.ilike(f"%{search}%"),
                Supplier.description.ilike(f"%{search}%"),
            )
        )

    total = query.count()

    query = apply_sorting(query, Supplier, sort_by, sort_order)

    query = apply_pagination(query, offset, page_size)

    items = query.all()

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": items,
    }



def get_supplier(db: Session, supplier_id: int):
    return db.query(Supplier).filter(Supplier.id == supplier_id).first()

def update_supplier(db: Session, supplier_id: int, data: SupplierCreate):
    supplier = get_supplier(db, supplier_id)
    if not supplier:
        return None
    for key, value in data.dict().items():
        setattr(supplier, key, value)
    db.commit()
    db.refresh(supplier)
    return supplier

def delete_supplier(db: Session, supplier_id: int):
    supplier = get_supplier(db, supplier_id)

    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")

    supplier.is_deleted = True
    db.commit()
    db.refresh(supplier)

    return supplier