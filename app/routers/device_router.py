from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.db_dependencies import get_db
from app.dependencies.device_dependencies import verify_device_id
from app.dependencies.user_dependencies import get_current_user
from app.models.device_model import DeviceModel
from app.models.user_model import UserModel
from app.schemas.device_schema import DeviceBase, DeviceResponse, DeviceUpdate
from app.services.device_services import (
    create_device,
    delete_device,
    get_all_devices,
    update_device,
    verify_device_create,
)

router = APIRouter()


@router.get("/")
async def get_devices(
    db: Session = Depends(get_db), user: UserModel = Depends(get_current_user)
):
    devices = get_all_devices(db, user)
    devices_res = [DeviceResponse.model_validate(d) for d in devices]
    return {"status": "success", "data": devices_res}


@router.get("/{device_id}")
async def get_device_by_id(device: DeviceModel = Depends(verify_device_id)):
    device_res = DeviceResponse.model_validate(device)
    return {"status": "Success", "data": device_res}


@router.post("/create")
async def create(
    device: DeviceBase,
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user),
):
    verify_device_create(db, device)
    new_device = create_device(db, device, user)
    return {
        "message": "Device created successfully",
        "device": new_device.serial_number,
    }


@router.put("/{device_id}")
async def update(
    device_update: DeviceUpdate,
    device: DeviceModel = Depends(verify_device_id),
    db: Session = Depends(get_db),
):
    device_updated = update_device(db, device_update, device)
    device_res = DeviceResponse.model_validate(device_updated)

    return {"message": "device successfully updated", "device": device_res}


@router.delete("/delete/{device_id}")
async def delete(
    device: DeviceModel = Depends(verify_device_id),
    db: Session = Depends(get_db),
):
    delete_device(db, device)
    return {"message": f"delete device {device.serial_number} success"}
