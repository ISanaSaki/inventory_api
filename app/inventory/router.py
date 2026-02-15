from fastapi import APIRouter, Depends, HTTPException,Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import require_role,pagination_params,sorting_params
from app.auth.service import get_current_user

from app.inventory import service
from app.inventory.schemas import InventoryCreate
from app.common.enums import Role,ChangeType

router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"],
    dependencies=[
        Depends(require_role([
            Role.ADMIN,
            Role.USER
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


@router.get("/")
def list_inventory(
    product_id: int | None = None,
    change_type: ChangeType | None = None,
    db: Session = Depends(get_db),
    pagination: dict = Depends(pagination_params),
    sorting: dict = Depends(sorting_params),
):
    return service.get_inventory_logs(
        db=db,
        page=pagination["page"],
        page_size=pagination["page_size"],
        offset=pagination["offset"],
        sort_by=sorting["sort_by"],
        sort_order=sorting["sort_order"],
        product_id=product_id,
        change_type=change_type,
    )