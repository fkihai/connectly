from fastapi import FastAPI
from fastapi.requests import Request

from .core.database import Base, engine
from .middlewares.auth import AuthMiddleware
from .routers import auth, user

app = FastAPI()

# migrate if not exist
Base.metadata.create_all(bind=engine)

# middleware
exclude = [
    "/auth/login",
    "/auth/register"
]
app.add_middleware(AuthMiddleware, excluded_paths=exclude)

# router
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(user.router, prefix="/user", tags=["User"])