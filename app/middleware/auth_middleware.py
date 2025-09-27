from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.security import verify_token


class AuthMiddleware(BaseHTTPMiddleware):

    def __init__(self, app, excluded_paths: list[str] = None):
        super().__init__(app)

        self.excluded_paths = excluded_paths or []

    async def dispatch(self, request, call_next):

        if request.url.path in self.excluded_paths:
            return await call_next(request)

        # extract token
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Missing or invalid Authorization header"},
            )

        token = auth_header.split(" ")[1]

        try:
            payload = verify_token(token)
            username = payload.get("sub")
            if username is None:
                raise HTTPException(status_code=401, detail="Invalid token payload")

            # for global state
            request.state.username = username

        except HTTPException as e:
            return JSONResponse(
                status_code=e.status_code,
                content={"status": "error", "message": e.detail, "data": None},
            )

        response = await call_next(request)
        return response
