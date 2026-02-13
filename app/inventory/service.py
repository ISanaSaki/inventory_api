from sqlalchemy.orm import Session
from app.inventory.models import Inventory
from app.products.models import Product
from app.inventory.schemas import InventoryCreate
from app.users.models import User
from app.audit.service import log_action
from app.common.enums import ChangeType

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

    log = Inventory(**data.dict())
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


def get_inventory_logs(db: Session, product_id: int = None, change_type: str = None):
    query = db.query(Inventory)
    if product_id is not None:
        query = query.filter(Inventory.product_id == product_id)
    if change_type is not None:
        query = query.filter(Inventory.change_type == change_type)
    return query.order_by(Inventory.created_at.desc()).all()