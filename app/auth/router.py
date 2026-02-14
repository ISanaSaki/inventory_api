from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.auth.schemas import LoginRequest, Token,TokenRefreshRequest
from app.auth.service import authenticate_user, create_user
from app.users.schemas import UserCreate, UserOut
from app.core.security import create_access_token,create_refresh_token,decode_access_token
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(
        db=db,
        email=user.email,
        password=user.password,
        role=user.role,
    )


@router.post("/login", response_model=Token)
def login(
    data: OAuth2PasswordRequestForm=Depends(),
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, data.username , data.password)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(
        {"sub": str(user.id), "role": user.role}
    )

    refresh_token = create_refresh_token(
        {"sub": str(user.id), "role": user.role}
    )   

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh", response_model=Token)
def refresh(data: TokenRefreshRequest):
    payload = decode_access_token(data.refresh_token)

    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    user_id = payload.get("sub")
    role = payload.get("role")

    new_access_token = create_access_token(
        {"sub": user_id, "role": role}
    )

    new_refresh_token = create_refresh_token(
        {"sub": user_id, "role": role}
    )

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }