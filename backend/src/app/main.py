import uvicorn
from fastapi import FastAPI

from api import router
from app.core.config import settings
from app.core.security import jwt_security, mfa_jwt_security

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    redoc_url=None,
)

jwt_security.handle_errors(app)
mfa_jwt_security.handle_errors(app)

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
