import os

import dotenv
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

BASE_DIR: str = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

if os.path.exists(os.path.join(BASE_DIR, ".env")):
    dotenv.load_dotenv(os.path.join(BASE_DIR, ".env"))

from app.common.security import jwt_security

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

jwt_security.handle_errors(app)

main_router = APIRouter(prefix="/api")

from app.api.routers import all_routers

for router in all_routers:
    main_router.include_router(router)

app.include_router(main_router)
