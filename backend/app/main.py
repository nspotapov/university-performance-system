from fastapi import FastAPI, APIRouter

from app.common.security import jwt_security

app = FastAPI()

jwt_security.handle_errors(app)

main_router = APIRouter(prefix="/api")

from app.api.routers import all_routers

for router in all_routers:
    main_router.include_router(router)

app.include_router(main_router)
