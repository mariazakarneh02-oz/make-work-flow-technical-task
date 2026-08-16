from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreateSchema(BaseModel):
    name: str
    email: EmailStr


class UserUpdateSchema(BaseModel):
    name: str | None = None
    email: EmailStr | None = None


class UserResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
    created_at: datetime
    updated_at: datetime