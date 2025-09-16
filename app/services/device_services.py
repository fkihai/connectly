from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.schemas.device_schema import DeviceBase
from app.models.device_model import DeviceModel
from app.models.user_model import UserModel


def verify_device(db: Session, device: DeviceBase):
    existing_device = (
        db.query(DeviceModel)
        .filter(DeviceModel.serial_number == device.serial_number)
        .first()
    )

    if existing_device:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"device with serial number {device.serial_number} already exists",
        )


def create_device(db: Session, device: DeviceBase, user: UserModel) -> DeviceModel:
    new_device = DeviceModel(**device.model_dump(exclude={"user_id"}))
    new_device.user_id = user.id

    db.add(new_device)
    db.commit()
    db.refresh(new_device)

    return new_device
