from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from app.enums.device_enum import DeviceType


class DeviceBase(BaseModel):
    serial_number: str
    name: str
    type: DeviceType


class DeviceUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None


class DeviceResponse(DeviceBase):
    id: UUID
    is_online: bool

    class Config:
        from_attributes = True
