from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import require_role
from app.auth.service import get_current_user

from app.inventory import service
from app.inventory.schemas import InventoryCreate
from app.common.enums import Role

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
    change_type: str | None = None,
    db: Session = Depends(get_db),
):
    return service.get_inventory_logs(
        db=db,
        product_id=product_id,
        change_type=change_type
    )