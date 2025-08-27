from fastapi import FastAPI, APIRouter

app = FastAPI()

main_router = APIRouter(prefix="/api")

from app.api.routers import all_routers

for router in all_routers:
    main_router.include_router(router)

app.include_router(main_router)

