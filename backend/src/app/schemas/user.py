# app/schemas/user.py

from uuid import UUID
from pydantic import BaseModel, ConfigDict, EmailStr


class UserBaseSchema(BaseModel):
    email: EmailStr


class UserRegisterSchema(UserBaseSchema):
    first_name: str
    last_name: str
    password: str


class UserLoginSchema(UserBaseSchema):
    password: str


class UserResponseSchema(UserBaseSchema):
    id: UUID
    first_name: str
    last_name: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class TokenResponseSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"
