from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.core.enum import UserRole


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str
    role: Optional[UserRole] = UserRole.user


class UserResponse(UserBase):
    id: int
    role: UserRole

    class Config:
        from_attributes = True
