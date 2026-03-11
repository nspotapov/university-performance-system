import logging
import uvicorn
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from api import router
from app.core.config import settings
from app.core.exceptions import ApplicationException
from app.core.security import jwt_security, mfa_jwt_security

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# List of endpoints to block from access logs
BLOCK_ENDPOINTS = ["/health"]

class EndpointFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        # Check if the log message contains any of the blocked endpoints
        for endpoint in BLOCK_ENDPOINTS:
            if endpoint in record.getMessage():
                return False
        return True
    
# Apply the filter to the 'uvicorn.access' logger
uvicorn_access_logger = logging.getLogger("uvicorn.access")
uvicorn_access_logger.addFilter(EndpointFilter())


@app.exception_handler(ApplicationException)
async def application_exception_handler(request: Request, ex: ApplicationException):  # noqa
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex))


jwt_security.handle_errors(app)
mfa_jwt_security.handle_errors(app)
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
