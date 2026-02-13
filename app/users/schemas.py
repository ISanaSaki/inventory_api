from pydantic import BaseModel,EmailStr
from app.common.enums import Role

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: Role=Role.USER


class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: Role
    is_active:bool
    is_verified:bool

    class Config:
        from_attributes = True
