from sqlalchemy.orm import Session
from app.audit.models import AuditLog
from app.core.query_utils import apply_pagination, apply_sorting
from fastapi.encoders import jsonable_encoder


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