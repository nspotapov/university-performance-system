from .auth_router import router as auth_router
from .users_router import router as router_users

all_routers = [
    router_users,
    auth_router
]
