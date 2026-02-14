from sqlalchemy.orm import Session
from sqlalchemy import func, case
from app.inventory.models import Inventory
from app.products.models import Product

def current_stock_report(db: Session):
    results = (
        db.query(
            Product.id.label("product_id"),
            Product.name.label("product_name"),
            func.coalesce(
                func.sum(
                    case(
                        (Inventory.change_type == "IN", Inventory.quantity),
                        else_=-Inventory.quantity,
                    )
                ),
                0
            ).label("current_stock")
        )
        .outerjoin(Inventory, Inventory.product_id == Product.id)
        .group_by(Product.id, Product.name)
        .all()
    )

    return [
        {
            "product_id": r.product_id,
            "product_name": r.product_name,
            "current_stock": float(r.current_stock),
        }
        for r in results
    ]

def low_stock_report(db: Session):
    results = (
        db.query(
            Product.id.label("product_id"),
            Product.name.label("product_name"),
            Product.min_quantity,
            func.coalesce(
                func.sum(
                    case(
                        (Inventory.change_type == "IN", Inventory.quantity),
                        else_=-Inventory.quantity,
                    )
                ),
                0
            ).label("current_stock")
        )
        .outerjoin(Inventory, Inventory.product_id == Product.id)
        .group_by(Product.id, Product.name, Product.min_quantity)
        .having(
            func.coalesce(
                func.sum(
                    case(
                        (Inventory.change_type == "IN", Inventory.quantity),
                        else_=-Inventory.quantity,
                    )
                ),
                0
            ) < Product.min_quantity
        )
        .all()
    )

    return [
        {
            "product_id": r.product_id,
            "product_name": r.product_name,
            "current_stock": float(r.current_stock),
            "min_quantity": r.min_quantity,
        }
        for r in results
    ]

def inventory_range_report(db: Session, start_date, end_date):
    results = (
        db.query(
            Inventory.change_type,
            func.coalesce(func.sum(Inventory.quantity), 0).label("total_quantity")
        )
        .filter(Inventory.created_at.between(start_date, end_date))
        .group_by(Inventory.change_type)
        .all()
    )

    data = {"IN": 0, "OUT": 0}

    for r in results:
        data[r.change_type] = float(r.total_quantity)

    return [
        {"change_type": key, "total_quantity": value}
        for key, value in data.items()
    ]


def top_products_report(db: Session, change_type: str):
    results = (
        db.query(
            Product.name.label("product_name"),
            func.sum(Inventory.quantity).label("total_quantity")
        )
        .join(Inventory, Inventory.product_id == Product.id)
        .filter(Inventory.change_type == change_type)
        .group_by(Product.name)
        .order_by(func.sum(Inventory.quantity).desc())
        .limit(5)
        .all()
    )

    return [
        {
            "product_name": r.product_name,
            "total_quantity": float(r.total_quantity),
        }
        for r in results
    ]