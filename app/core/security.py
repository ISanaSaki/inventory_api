from datetime import datetime, timedelta,timezone
from uuid import uuid4
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import HTTPException, status
from app.core.config import settings
import hmac,hashlib
from datetime import datetime, timezone

def exp_to_datetime(exp: int) -> datetime:
    return datetime.fromtimestamp(exp, tz=timezone.utc)

pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)

def _now() -> datetime:
    return datetime.now(timezone.utc)

def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None
) -> str:
    to_encode = data.copy()

    now = datetime.now(timezone.utc)
    expire = now + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))

    to_encode.update({
        "type": "access",
        "exp": int(expire.timestamp()),
        "iat": int(now.timestamp()),
        "nbf": int(now.timestamp()),
        "jti": str(uuid4()),
        "iss": settings.JWT_ISSUER,
        "aud": settings.JWT_AUDIENCE,
    })

    return jwt.encode(
        to_encode,
        settings.ACCESS_TOKEN_SECRET_KEY,
        algorithm=settings.ALGORITHM
    )


def decode_access_token(token: str, token_type: str = "access") -> dict:
    try:
        secret = (
            settings.ACCESS_TOKEN_SECRET_KEY
            if token_type == "access"
            else settings.REFRESH_TOKEN_SECRET_KEY
        )

        payload = jwt.decode(
            token,
            secret,
            algorithms=[settings.ALGORITHM],
            audience=settings.JWT_AUDIENCE,
            issuer=settings.JWT_ISSUER,
            options={"require_aud": True, "require_iss": True},
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    if payload.get("type") != token_type:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type"
        )

    return payload
    

def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()

    now = datetime.now(timezone.utc)
    expire = now + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    to_encode.update({
        "type": "refresh",
        "exp": int(expire.timestamp()),
        "iat": int(now.timestamp()),
        "nbf": int(now.timestamp()),
        "jti": str(uuid4()),
        "iss": settings.JWT_ISSUER,
        "aud": settings.JWT_AUDIENCE,
    })

    return jwt.encode(
        to_encode,
        settings.REFRESH_TOKEN_SECRET_KEY, 
        algorithm=settings.ALGORITHM
    )

def hash_refresh_token(raw_token: str) -> str:
    return hmac.new(
        settings.REFRESH_TOKEN_SECRET_KEY.encode(),
        raw_token.encode(),
        hashlib.sha256
    ).hexdigest()

