from sqlalchemy.orm import Session
from app.audit.models import AuditLog


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