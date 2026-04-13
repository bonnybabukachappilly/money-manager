from fastapi import APIRouter

from .router.auth import router as auth_router
from .router.user import router as user_router
from .router.accounts import router as account_router
from .router.categories import router as category_router


v1_router = APIRouter(prefix='/api/v1')
v1_router.include_router(auth_router)
v1_router.include_router(user_router)
v1_router.include_router(account_router)
v1_router.include_router(category_router)
