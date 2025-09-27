import enum

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class ChannelPatternModel(Base):
    __tablename__ = "channels_patterns"
    id = Column(Integer, primary_key=True, index=True)
    channel_id = Column(Integer, ForeignKey("channels.id"))
    field_name = Column(String, nullable=True)
    field_type = Column(String, nullable=True)
    required = Column(Boolean, default=False)
    default_value = Column(String, nullable=False)
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
    channel = relationship("ChannelModel", back_populates="channel_patterns")
