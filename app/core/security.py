from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from jose import ExpiredSignatureError, JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

# password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"])

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Token Expired"},
            headers={"WWW-Authenticate": "Bearer"},
        )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, password: str) -> bool:
    return pwd_context.verify(plain_password, password)
