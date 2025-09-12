from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.models.user_model import UserModel


def get_user_by_username(username: str, db: Session) -> UserModel:

    user = db.query(UserModel).filter(UserModel.username == username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"status": "error", "message": "User not found"},
        )

    return user
