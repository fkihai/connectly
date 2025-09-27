import enum

from sqlalchemy import Column, DateTime, Enum, Integer, String, func
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.enums.role_enum import UserRole


class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(Enum(UserRole, name="user_role"), default=UserRole.user)
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
    devices = relationship("DeviceModel", back_populates="user")
