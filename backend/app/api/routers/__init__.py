from .auth_router import router as auth
from .users_router import router as users
from .common_router import router as common

all_routers = [
    users,
    auth,
    common
]
