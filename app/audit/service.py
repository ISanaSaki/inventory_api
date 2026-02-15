from sqlalchemy.orm import Session
from app.audit.models import AuditLog
from app.core.query_utils import apply_pagination, apply_sorting
from app.audit.models import AuditLog


def get_audit_logs(
    db: Session,
    page: int,
    page_size: int,
    offset: int,
    sort_by: str | None,
    sort_order: str,
    user_id: int | None = None,
    entity: str | None = None,
):
    query = db.query(AuditLog)

    if user_id:
        query = query.filter(AuditLog.user_id == user_id)

    if entity:
        query = query.filter(AuditLog.entity == entity)

    total = query.count()

    if not sort_by:
        sort_by = "created_at"
        sort_order = "desc"

    query = apply_sorting(query, AuditLog, sort_by, sort_order)
    query = apply_pagination(query, offset, page_size)

    items = query.all()

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": items,
    }


def log_action(
    db: Session,
    user_id: int | None,
    action: str,
    entity: str,
    entity_id: int | None = None,
    old_data: dict | None = None,
    new_data: dict | None = None,
):
    log = AuditLog(
        user_id=user_id,
        action=action,
        entity=entity,
        entity_id=entity_id,
        old_data=old_data,
        new_data=new_data,
    )
    db.add(log)
    db.commit()