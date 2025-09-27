from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.dependencies.db_dependencies import get_db
from app.dependencies.user_dependencies import get_current_user
from app.models.user_model import UserModel
from app.schemas.user_schema import UserResponse
from app.services.user_services import get_user_by_username

router = APIRouter()


@router.get("/info")
async def user_info(request: Request, user: UserModel = Depends(get_current_user)):
    user_detail = UserResponse.model_validate(user)
    return {"status": "success", "data": user_detail}
