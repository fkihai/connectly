from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import get_password_hash
from app.enums.role_enum import UserRole
from app.models.user_model import UserModel
from app.schemas.user_schema import UserCreate


def get_user_by_username(username: str, db: Session) -> UserModel:

    user = db.query(UserModel).filter(UserModel.username == username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"status": "error", "message": "User not found"},
        )

    return user


def create_user(db: Session, user_data: UserCreate) -> UserModel:
    new_user = UserModel(**user_data.model_dump(exclude={"password"}))
    new_user.password = get_password_hash(user_data.password)

    # Add the new user to the database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def create_superuser(db: Session) -> None:
    user = (
        db.query(UserModel)
        .filter(UserModel.username == settings.SUPERUSER_USERNAME)
        .first()
    )

    if not user:
        user_in = UserModel(
            username=settings.SUPERUSER_USERNAME,
            password=get_password_hash(settings.SUPERUSER_PASSWORD),
            email=settings.SUPERUSER_EMAIL,
            role=UserRole.admin,
        )

        db.add(user_in)
        db.commit()
        db.refresh(user_in)

        print(f"✅ Superuser '{settings.SUPERUSER_USERNAME}' success created.")
