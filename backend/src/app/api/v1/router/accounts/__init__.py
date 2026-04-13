from fastapi import APIRouter

from .standard import router as account_router
from .credit import router as credit_router
from .recurring import router as loan_router


router = APIRouter(prefix='/accounts')
router.include_router(account_router)
router.include_router(credit_router)
router.include_router(loan_router)
