from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.rate_limiter import limiter

from app.auth.schemas import Token, TokenRefreshRequest
from app.auth.service import authenticate_user, create_user
from app.users.schemas import UserCreate, UserOut

from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_access_token,
    hash_refresh_token,
    exp_to_datetime,
)

from app.auth.models import RefreshToken
from app.users.models import User

from app.core.password_policy import validate_password
from app.services.auth_security import is_locked, register_failed_login, register_success_login

from app.auth.models import LoginAttempt 

from app.audit.models import AuditLog
from datetime import datetime, timezone


router = APIRouter(prefix="/auth", tags=["Auth"])

INVALID_CREDENTIALS_MSG = "Invalid credentials"


def client_ip(request: Request) -> str | None:

    xff = request.headers.get("x-forwarded-for")
    if xff:
        return xff.split(",")[0].strip()
    return request.client.host if request.client else None


def log_login_attempt(db: Session, identifier: str, user_id: int | None, success: bool, request: Request):
    db.add(
        LoginAttempt(
            identifier=identifier,
            user_id=user_id,
            success=success,
            ip=client_ip(request),
            user_agent=request.headers.get("user-agent"),
        )
    )

def revoke_all_refresh_tokens(db: Session, user_id: int, request: Request, reason: str):
    db.query(RefreshToken).filter(
        RefreshToken.user_id == user_id,
        RefreshToken.revoked.is_(False),
    ).update({"revoked": True}, synchronize_session=False)

    db.add(
        AuditLog(
            user_id=user_id,
            action="TOKEN_REUSE_DETECTED",
            entity="auth",
            entity_id=user_id,
            new_data={
                "ip": client_ip(request),
                "user_agent": request.headers.get("user-agent"),
                "reason": reason,
            },
        )
    )

@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):

    try:
        validate_password(user.password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return create_user(
        db=db,
        email=user.email,
        password=user.password,
        role=user.role,
    )


@router.post("/login", response_model=Token)
@limiter.limit("5/minute")
def login(request: Request, data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    identifier = (data.username or "").strip().lower()

    user = db.query(User).filter(User.email == identifier).first()

    if user and is_locked(user):
        log_login_attempt(db, identifier, user.id, False, request)
        db.commit()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=INVALID_CREDENTIALS_MSG)

    authed = authenticate_user(db, identifier, data.password)

    if not authed:
        if user:
            register_failed_login(user)
        log_login_attempt(db, identifier, user.id if user else None, False, request)
        db.commit()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=INVALID_CREDENTIALS_MSG)

    register_success_login(user)
    log_login_attempt(db, identifier, user.id, True, request)

    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})

    refresh_payload = decode_access_token(refresh_token, token_type="refresh")
    refresh_jti = refresh_payload["jti"]
    expires_at = exp_to_datetime(refresh_payload["exp"])

    db.add(
        RefreshToken(
            user_id=user.id,
            jti=refresh_jti,
            token_hash=hash_refresh_token(refresh_token),
            expires_at=expires_at,
            revoked=False,
        )
    )
    db.commit()

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.post("/refresh", response_model=Token)
@limiter.limit("10/minute")
def refresh(request: Request, data: TokenRefreshRequest, db: Session = Depends(get_db)):
    try:
        payload = decode_access_token(data.refresh_token, token_type="refresh")
    except HTTPException:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=INVALID_CREDENTIALS_MSG)

    user_id = int(payload["sub"])
    jti = payload["jti"]

    rt = db.query(RefreshToken).filter(RefreshToken.jti == jti).first()

    if not rt:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=INVALID_CREDENTIALS_MSG)
    if rt.expires_at and rt.expires_at < datetime.now(timezone.utc):
        rt.revoked = True
        db.commit()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=INVALID_CREDENTIALS_MSG)

    if rt.revoked:
        revoke_all_refresh_tokens(db, user_id=user_id, request=request, reason="revoked_token_presented")
        db.commit()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=INVALID_CREDENTIALS_MSG)

    if rt.token_hash != hash_refresh_token(data.refresh_token):
        revoke_all_refresh_tokens(db, user_id=user_id, request=request, reason="token_hash_mismatch")
        db.commit()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=INVALID_CREDENTIALS_MSG)

    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=INVALID_CREDENTIALS_MSG)

    rt.revoked = True

    new_access_token = create_access_token({"sub": str(user.id)})
    new_refresh_token = create_refresh_token({"sub": str(user.id)})

    new_payload = decode_access_token(new_refresh_token, token_type="refresh")
    new_expires_at = exp_to_datetime(new_payload["exp"])
    new_jti = new_payload["jti"]

    db.add(
        RefreshToken(
            user_id=user.id,
            jti=new_jti,
            token_hash=hash_refresh_token(new_refresh_token),
            expires_at=new_expires_at,
            revoked=False,
        )
    )
    db.commit()

    return {"access_token": new_access_token, "refresh_token": new_refresh_token, "token_type": "bearer"}