from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from app.core.database import get_db
from app.reports.schemas import CurrentStockOut
from app.reports.service import (
    current_stock_report,
    low_stock_report,
    inventory_range_report,
    top_products_report
)
from app.core.dependencies import require_role
from app.common.enums import Role

router = APIRouter(
    prefix="/reports",
    tags=["reports"],
    dependencies=[
        Depends(require_role([Role.ADMIN]))
    ]
)
@router.get("/current-stock", response_model=list[CurrentStockOut])
def current_stock(db: Session = Depends(get_db)):
    return current_stock_report(db)

@router.get("/low-stock")
def low_stock(db: Session = Depends(get_db)):
    return low_stock_report(db)

@router.get("/inventory-range")
def inventory_range(start: datetime, end: datetime, db: Session = Depends(get_db)):
    return inventory_range_report(db, start, end)

@router.get("/top-in")
def top_in(db: Session = Depends(get_db)):
    return top_products_report(db, "IN")

@router.get("/top-out")
def top_out(db: Session = Depends(get_db)):
    return top_products_report(db, "OUT")