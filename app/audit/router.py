from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.audit.models import AuditLog
from app.core.dependencies import require_role
from app.common.enums import Role
from app.core.dependencies import pagination_params,sorting_params
from app.audit import service

router = APIRouter(
    prefix="/audit",
    tags=["Audit"],
    dependencies=[
        Depends(require_role([Role.ADMIN]))
    ]
)


@router.get("/")
def list_audit_logs(
    user_id: int | None = None,
    entity: str | None = None,
    db: Session = Depends(get_db),
    pagination: dict = Depends(pagination_params),
    sorting: dict = Depends(sorting_params),
):
    return service.get_audit_logs(
        db=db,
        page=pagination["page"],
        page_size=pagination["page_size"],
        offset=pagination["offset"],
        sort_by=sorting["sort_by"],
        sort_order=sorting["sort_order"],
        user_id=user_id,
        entity=entity,
    )
