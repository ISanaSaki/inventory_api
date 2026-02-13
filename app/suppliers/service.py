from sqlalchemy.orm import Session
from app.suppliers.models import Supplier
from app.suppliers.schemas import SupplierCreate

def create_supplier(db: Session, data: SupplierCreate):
    supplier = Supplier(**data.dict())
    db.add(supplier)
    db.commit()
    db.refresh(supplier)
    return supplier

def get_suppliers(db: Session):
    return db.query(Supplier).all()

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
        return None
    db.delete(supplier)
    db.commit()
    return supplier