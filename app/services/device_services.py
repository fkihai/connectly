from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.enums.device_enum import DeviceType
from app.models.device_model import DeviceModel
from app.models.user_model import UserModel
from app.schemas.device_schema import DeviceBase, DeviceUpdate


def get_all_devices(db: Session, user: UserModel) -> list[DeviceModel]:
    devices = db.query(DeviceModel).filter(DeviceModel.user_id == user.id).all()
    return devices


def verify_device_create(db: Session, device: DeviceBase):
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


def update_device(
    db: Session, device_update: DeviceUpdate, device: DeviceModel
) -> DeviceModel:
    update_data = device_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        verify_device_type(key, value)
        setattr(device, key, value)

    db.commit()
    db.refresh(device)

    return device


def delete_device(db: Session, device: DeviceModel):
    db.delete(device)
    db.commit()


def verify_device_type(key: str, value: str):
    if key == "type":
        if value not in DeviceType._value2member_map_:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid Device type {value}",
            )
