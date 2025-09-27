import enum

from sqlalchemy import Column, DateTime, Integer, String, Text, func
from sqlalchemy.orm import relationship

from app.core.database import Base


class ChannelModel(Base):
    __tablename__ = "channels"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(Text, nullable=True)
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
    channel_patterns = relationship("ChannelPatternModel", back_populates="channel")
