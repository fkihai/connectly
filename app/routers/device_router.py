from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.device_schema import DeviceBase
from app.models.user_model import UserModel
from app.dependencies.db_dependency import get_db
from app.dependencies.user_dependency import get_current_user
from app.services.device_services import create_device, verify_device

router = APIRouter()


@router.post("/")
async def info():
    pass


@router.post("/create")
async def create(
    device: DeviceBase,
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user),
):
    verify_device(db, device)
    new_device = create_device(db, device, user)
    return {
        "message": "Device created successfully",
        "device": new_device.serial_number,
    }


@router.post("/update")
async def update():
    pass


@router.post("/delete")
async def delete():
    pass
