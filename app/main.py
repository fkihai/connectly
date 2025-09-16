from fastapi import FastAPI
from fastapi.requests import Request

from .core.db_init import Base, engine
from .middlewares.auth_middleware import AuthMiddleware
from .routers import auth_router, user_router, device_router

app = FastAPI()

# middleware
exclude = ["/auth/login"]
app.add_middleware(AuthMiddleware, excluded_paths=exclude)

# router
app.include_router(auth_router.router, prefix="/auth", tags=["Auth"])
app.include_router(user_router.router, prefix="/user", tags=["User"])
app.include_router(device_router.router, prefix="/device", tags=["Device"])
