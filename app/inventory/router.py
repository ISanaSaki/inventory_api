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
from app.inventory.service import Inventory
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


def get_inventory_logs(
    db,
    change_type=None,
    product_id=None,
    user_id=None,
    supplier_id=None,
    start_date=None,
    end_date=None,

    # pagination
    page: int = 1,
    page_size: int = 20,
    offset: int | None = None,

    # sorting
    sort_by: str = "created_at",
    sort_order: str = "desc",
):
    q = db.query(Inventory).filter(Inventory.is_deleted == False)

    # ✅ change_type: Enum or str
    if change_type:
        if isinstance(change_type, ChangeType):
            change_type = change_type.value  # "IN" or "OUT"

        if change_type not in ("IN", "OUT"):
            raise HTTPException(status_code=400, detail="Invalid change_type")

        q = q.filter(Inventory.change_type == change_type)

    if product_id:
        q = q.filter(Inventory.product_id == product_id)

    if user_id:
        q = q.filter(Inventory.user_id == user_id)

    if supplier_id:
        q = q.filter(Inventory.supplier_id == supplier_id)

    if start_date:
        q = q.filter(Inventory.created_at >= start_date)

    if end_date:
        q = q.filter(Inventory.created_at <= end_date)

    total = q.count()

    # sorting
    allowed_sort_fields = {"created_at", "quantity", "id", "product_id", "user_id"}
    if sort_by not in allowed_sort_fields:
        raise HTTPException(status_code=400, detail="Invalid sort_by")

    sort_col = getattr(Inventory, sort_by)
    if sort_order == "asc":
        q = q.order_by(sort_col.asc())
    else:
        q = q.order_by(sort_col.desc())

    #  pagination
    if offset is None:
        offset = (page - 1) * page_size

    items = q.offset(offset).limit(page_size).all()

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": items
    }

@router.get("/history", response_model=InventoryList)
def get_history(
    change_type: Optional[str] = None,
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