from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.dependencies.db_dependencies import get_db
from app.enums.role_enum import UserRole
from app.models.user_model import UserModel
from app.services.user_services import get_user_by_username


def get_current_user(request: Request, db: Session = Depends(get_db)) -> UserModel:
    username = request.state.username
    user = get_user_by_username(username, db)
    return user


def role_required(*role: UserRole):
    def dependency(current_user: UserModel = Depends(get_current_user)):
        if current_user.role not in role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="only admin can create user",
            )
        return current_user

    return dependency
