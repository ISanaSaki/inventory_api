from fastapi import APIRouter, Depends, HTTPException,Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import require_role,pagination_params,sorting_params
from app.auth.service import get_current_user

from app.inventory import service
from app.inventory.schemas import InventoryCreate
from app.common.enums import Role,ChangeType
from typing import Optional
from datetime import datetime
from app.users.models import User
from app.inventory.schemas import InventoryList

router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"],
    dependencies=[
        Depends(require_role([
           Role.ADMIN,
            Role.STAFF
        ]))
    ]
)


@router.post("/")
def create_inventory(
    data: InventoryCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    try:
        return service.create_inventory_log(
            db=db,
            data=data,
            current_user=current_user
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/history", response_model=InventoryList)
def get_history(
    change_type: ChangeType | None = Query(None),
    product_id: Optional[int] = None,
    user_id: Optional[int] = None,
    supplier_id: Optional[int] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.get_inventory_logs(
        db=db,
        change_type=change_type,
        product_id=product_id,
        user_id=user_id,
        supplier_id=supplier_id,
        start_date=start_date,
        end_date=end_date,
        page=page,
        page_size=page_size,
    )