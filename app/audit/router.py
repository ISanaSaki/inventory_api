from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.audit.models import AuditLog
from app.core.dependencies import require_role
from app.common.enums import Role

router = APIRouter(
    prefix="/audit",
    tags=["Audit"],
    dependencies=[
        Depends(require_role([Role.ADMIN]))
    ]
)


@router.get("/")
def get_logs(db: Session = Depends(get_db)):
    return db.query(AuditLog).order_by(AuditLog.created_at.desc()).all()