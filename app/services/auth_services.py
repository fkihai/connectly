from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.security import create_access_token, verify_password
from app.models.user_model import UserModel
from app.schemas.user_schema import UserCreate
from app.services.user_services import get_user_by_username


def authenticate_user(db: Session, username: str, password: str) -> UserModel | None:
    user = get_user_by_username(username, db)
    if not user or not verify_password(password, user.password):
        return None
    return user


def login_for_access_token(
    db: Session, form_data: OAuth2PasswordRequestForm
) -> tuple[str, UserModel]:

    user = authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.username})

    return access_token, user


def verify_user_already_exists(db: Session, user_data: UserCreate):
    existing_user = (
        db.query(UserModel).filter(UserModel.username == user_data.username).first()
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
        )
