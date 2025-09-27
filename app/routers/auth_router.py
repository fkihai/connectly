from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.dependencies.db_dependencies import get_db
from app.dependencies.user_dependencies import role_required
from app.enums.role_enum import UserRole
from app.schemas.user_schema import UserCreate, UserResponse
from app.services import auth_services, user_services

router = APIRouter()


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    access_token, user = auth_services.login_for_access_token(db, form_data)
    user_data = UserResponse.model_validate(user)

    return {
        "user": user_data,
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.post("/register")
def register(
    user: UserCreate,
    role: UserRole = Depends(role_required(UserRole.admin)),
    db: Session = Depends(get_db),
):
    auth_services.verify_user_already_exists(db, user)
    new_user = user_services.create_user(db, user)
    return {"message": "User created successfully", "user_id": new_user.id}
