from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.dependencies.db_dependency import get_db
from app.models.user_model import UserModel
from app.schemas.user_schema import UserCreate, UserResponse
from app.services.auth_service import (
    authenticate_user,
    create_access_token,
    get_password_hash,
)

router = APIRouter()


@router.post("/login")
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.username})
    user_data = UserResponse.model_validate(user)

    return {
        "user": user_data,
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.post("/logout")
def logout():
    pass


@router.post("/register")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if the username already exists
    existing_user = (
        db.query(UserModel).filter(UserModel.username == user.username).first()
    )
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
        )

    password = get_password_hash(user.password)
    # Create a new user object
    new_user = UserModel(username=user.username, email=user.email, password=password)
    # Add the new user to the database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully", "user_id": new_user.id}
