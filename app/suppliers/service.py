from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.suppliers.models import Supplier
from app.suppliers.schemas import SupplierCreate

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

def get_suppliers(db: Session):
    return db.query(Supplier).filter(Supplier.is_deleted == False).all()

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