from .auth_controller import auth_router
from .user_controller import user_router

routers = [
    user_router,
    auth_router
]
