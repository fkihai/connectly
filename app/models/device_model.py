import uuid

from sqlalchemy import (
    UUID,
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    func,
)
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.enums.device_enum import DeviceType


class DeviceModel(Base):
    __tablename__ = "devices"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    serial_number = Column(String, unique=True, nullable=False)
    name = Column(String, index=True)
    type = Column(Enum(DeviceType, name="device_type"), default=DeviceType.mqtt)
    is_online = Column(Boolean, nullable=False, default=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # relationship with user
    user = relationship("UserModel", back_populates="devices")
    sensors = relationship("SensorModel", back_populates="device")
