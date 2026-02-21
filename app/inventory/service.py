from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.inventory.models import Inventory
from app.products.models import Product
from app.inventory.schemas import InventoryCreate
from app.users.models import User
from app.audit.service import log_action
from app.common.enums import ChangeType
from app.core.query_utils import apply_pagination,apply_sorting

def get_current_stock(db: Session, product_id: int):
    result = db.query(
        Inventory.change_type,
        Inventory.quantity
    ).filter(Inventory.product_id == product_id).all()

    stock = 0
    for change_type, qty in result:
        if change_type == ChangeType.IN:
            stock += qty
        else:
            stock -= qty
    return stock


def create_inventory_log(
    db: Session,
    data: InventoryCreate,
    current_user: User
):
    if data.quantity <= 0:
        raise ValueError("Quantity must be positive")

    previous_stock = get_current_stock(db, data.product_id)

    if data.change_type == ChangeType.OUT:
        if data.quantity > previous_stock:
            raise ValueError("Not enough stock")

    payload = data.dict() 
    payload["user_id"] = current_user.id
    log = Inventory(**payload)
    db.add(log)
    db.commit()
    db.refresh(log)

    new_stock = get_current_stock(db, data.product_id)

    log_action(
        db=db,
        user_id=current_user.id,
        action="STOCK_IN" if data.change_type == ChangeType.IN else "STOCK_OUT",
        entity="inventory",
        entity_id=data.product_id,
        old_data={
            "previous_stock": previous_stock
        },
        new_data={
            "quantity": data.quantity,
            "current_stock": new_stock
        }
    )

    return log

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
    q = db.query(Inventory)
    # change_type: Enum or str
    if change_type:
        if isinstance(change_type, str):
            try:
                change_type = ChangeType(change_type)
            except ValueError:
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

    #  sorting 
    allowed_sort_fields = {"created_at", "quantity", "id", "product_id", "user_id"}
    if sort_by not in allowed_sort_fields:
        raise HTTPException(status_code=400, detail="Invalid sort_by")

    sort_col = getattr(Inventory, sort_by)
    if sort_order == "asc":
        q = q.order_by(sort_col.asc())
    else:
        q = q.order_by(sort_col.desc())

    # pagination
    if offset is None:
        offset = (page - 1) * page_size

    items = q.offset(offset).limit(page_size).all()

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": items
    }