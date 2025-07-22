from fastapi import FastAPI, APIRouter

app = FastAPI()

main_router = APIRouter(prefix="/api")

from app.controllers import routers

for router in routers:
    main_router.include_router(router)

app.include_router(main_router)
