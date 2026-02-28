from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from app.common.security import jwt_security
from app.api.routers import all_routers
import app.config

show_docs = app.config.debug

app = FastAPI(
    docs_url="/api/swagger" if show_docs else None,
    openapi_url="/api/openapi.json" if show_docs else None,
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

jwt_security.handle_errors(app)

main_router = APIRouter(prefix="/api")


for router in all_routers:
    main_router.include_router(router)

app.include_router(main_router)
