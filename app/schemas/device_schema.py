from pydantic import BaseModel

from app.core.enum import DeviceType


class DeviceBase(BaseModel):
    serial_number: str
    name: str
    type: DeviceType


class DeviceResponse(DeviceBase):
    id: str
    is_online: bool

    class config:
        from_attributes: True
