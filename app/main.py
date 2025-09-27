from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi.requests import Request
from sqlalchemy.orm import Session, Session


from .core.database import Base, engine, SessionLocal
from .dependencies.db_dependencies import get_db
from .middleware.auth_middleware import AuthMiddleware
from .routers import auth_router, device_router, user_router
from .services.user_services import create_superuser


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = SessionLocal()
    try:
        create_superuser(db)
    finally:
        db.close()
    yield
    print("🛑 App stopped")


app = FastAPI(lifespan=lifespan)

# middleware
exclude = ["/auth/login"]
app.add_middleware(AuthMiddleware, excluded_paths=exclude)

# router
app.include_router(auth_router.router, prefix="/auth", tags=["Auth"])
app.include_router(user_router.router, prefix="/users", tags=["User"])
app.include_router(device_router.router, prefix="/devices", tags=["Device"])


"""
TODO TEST:
1. tes create user
2. tes login user
3. tes middleware
4. tes crud device
5. tes post config and reponse
6. tes store data
"""
