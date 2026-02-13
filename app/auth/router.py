from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.auth.schemas import LoginRequest, Token
from app.auth.service import authenticate_user, create_user
from app.users.schemas import UserCreate, UserOut
from app.core.security import create_access_token
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

    token = create_access_token({"sub": str(user.id), "role": user.role})
    return {"access_token": token}