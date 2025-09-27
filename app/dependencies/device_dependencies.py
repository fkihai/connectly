from uuid import UUID

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies.db_dependencies import get_db
from app.models.device_model import DeviceModel


def verify_device_id(device_id: UUID, db: Session = Depends(get_db)) -> DeviceModel:
    device = db.query(DeviceModel).filter(DeviceModel.id == device_id).first()

    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    return device
