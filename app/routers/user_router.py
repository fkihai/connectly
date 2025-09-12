from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.dependencies.db_dependency import get_db
from app.models.user_model import UserModel
from app.schemas.user_schema import UserResponse
from app.services.user_service import get_user_by_username

router = APIRouter()


@router.get("/info")
async def user_info(request: Request, db: Session = Depends(get_db)):

    username = request.state.username
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"status": "error", "message": "User not found"},
        )

    user = get_user_by_username(username, db)
    user_detail = UserResponse.model_validate(user)

    return {"status": "success", "data": user_detail}
