import enum

from sqlalchemy import (
    JSON,
    UUID,
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
from app.enums.device_enum import DataType


class SensorModel(Base):
    __tablename__ = "sensors"
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(UUID(as_uuid=True), ForeignKey("devices.id"))
    key = Column(String, nullable=False)
    channel = Column(String, nullable=False)
    data_type = Column(Enum(DataType, name="data_type"), nullable=False)
    config = Column(Enum(DataType, name="data_type"), nullable=False)
    role = Column(JSON, nullable=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # relationship
    device = relationship("DeviceModel", back_populates="sensors")
