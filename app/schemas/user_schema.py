from typing import List, Optional

from pydantic import BaseModel

from app.enums.role_enum import UserRole
from app.schemas.device_schema import DeviceResponse


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


class UserWithDeviceResponse(UserResponse):
    devices: List[DeviceResponse]
