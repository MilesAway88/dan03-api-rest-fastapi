from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    nombre: str
    email: str


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    created_at: datetime

    # Convierte objetos de SQLAlchemy a Pydantic automáticamente
    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: str | None = None