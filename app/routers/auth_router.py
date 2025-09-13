from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.dependencies.db_dependency import get_db
from app.models.user_model import UserModel
from app.schemas.user_schema import UserCreate, UserResponse
from app.services.auth_service import (
    authenticate_user,
    create_access_token,
    create_user,
    verify_user_already_exists,
    login_for_access_token,
)

router = APIRouter()


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    access_token, user = login_for_access_token(db, form_data)
    user_data = UserResponse.model_validate(user)

    return {
        "user": user_data,
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    verify_user_already_exists(db, user)
    new_user = create_user(db, user)
    return {"message": "User created successfully", "user_id": new_user.id}
