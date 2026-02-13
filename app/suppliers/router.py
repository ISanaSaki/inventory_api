from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.suppliers.schemas import SupplierCreate, SupplierOut
from app.suppliers.service import create_supplier, get_suppliers, get_supplier, update_supplier, delete_supplier
from app.core.dependencies import require_role
from app.common.enums import Role

router = APIRouter(
    prefix="/suppliers",
    tags=["Suppliers"],
    dependencies=[
        Depends(require_role([Role.ADMIN]))
    ]
)

@router.post("/", response_model=SupplierOut)
def add_supplier(data: SupplierCreate, db: Session = Depends(get_db)):
    return create_supplier(db, data)

@router.get("/", response_model=list[SupplierOut])
def list_suppliers(db: Session = Depends(get_db)):
    return get_suppliers(db)

@router.get("/{supplier_id}", response_model=SupplierOut)
def retrieve_supplier(supplier_id: int, db: Session = Depends(get_db)):
    supplier = get_supplier(db, supplier_id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return supplier

@router.put("/{supplier_id}", response_model=SupplierOut)
def update_supplier_router(supplier_id: int, data: SupplierCreate, db: Session = Depends(get_db)):
    updated = update_supplier(db, supplier_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return updated

@router.delete("/{supplier_id}", response_model=SupplierOut)
def delete_supplier_router(supplier_id: int, db: Session = Depends(get_db)):
    deleted = delete_supplier(db, supplier_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return deleted