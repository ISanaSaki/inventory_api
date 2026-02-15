from enum import Enum
from fastapi import Depends, HTTPException, status,Query
from typing import Optional
from app.users.models import User
from app.auth.service import get_current_user
from app.common.enums import Role

def require_role(allowed_roles: list[Role]):
    def checker(current_user: User = Depends(get_current_user)):
        user_role = Role(current_user.role)
        if user_role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        return current_user
    return checker


def pagination_params(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
):
    return {
        "page": page,
        "page_size": page_size,
        "offset": (page - 1) * page_size,
    }


def sorting_params(
    sort_by: Optional[str] = Query(None),
    sort_order: Optional[str] = Query("asc"),
):
    return {
        "sort_by": sort_by,
        "sort_order": sort_order,
    }