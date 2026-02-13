from enum import Enum
from fastapi import Depends, HTTPException, status
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
