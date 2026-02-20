from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.audit.models import AuditLog
from app.core.query_utils import apply_pagination, apply_sorting

def log_action(
    db: Session,
    user_id: int | None,
    action: str,
    entity: str,
    entity_id: int | None = None,
    old_data: dict | None = None,
    new_data: dict | None = None,
):
    old_data_json = jsonable_encoder(old_data) if old_data is not None else None
    new_data_json = jsonable_encoder(new_data) if new_data is not None else None

    log = AuditLog(
        user_id=user_id,
        action=action,
        entity=entity,
        entity_id=entity_id,
        old_data=old_data_json,
        new_data=new_data_json,
    )
    db.add(log)
    db.commit()

def get_audit_logs(
    db: Session,
    page: int,
    page_size: int,
    offset: int,
    sort_by: str | None = None,
    sort_order: str = "desc",
    user_id: int | None = None,
    action: str | None = None,
    entity: str | None = None,
    entity_id: int | None = None,
):
    q = db.query(AuditLog)
    if user_id is not None:
        q = q.filter(AuditLog.user_id == user_id)
    if action is not None:
        q = q.filter(AuditLog.action == action)
    if entity is not None:
        q = q.filter(AuditLog.entity == entity)
    if entity_id is not None:
        q = q.filter(AuditLog.entity_id == entity_id)

    q = apply_sorting(q, AuditLog, sort_by, sort_order)
    q = apply_pagination(q, page_size=page_size, offset=offset)

    return q.all()