from pydantic import BaseModel,EmailStr,field_validator
from app.common.enums import Role

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: Role=Role.USER
    @field_validator("password")
    @classmethod
    def strong_password(cls, v: str):
        if len(v) < 10:
            raise ValueError("Password too short (min 10)")
        return v


class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: Role
    is_active:bool
    is_verified:bool

    class Config:
        from_attributes = True
