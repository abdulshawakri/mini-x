from uuid import UUID

from pydantic import BaseModel, EmailStr, SecretStr, ConfigDict


class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None
    street_address: str | None = None
    zip_code: str | None = None
    city: str | None = None
    country: str | None = None


class UserUpdate(BaseModel):
    full_name: str | None = None
    street_address: str | None = None
    zip_code: str | None = None
    city: str | None = None
    country: str | None = None


class UserCreate(UserBase):
    password: SecretStr


class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
