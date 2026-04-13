# app/api/v1/routers/users.py

from fastapi import APIRouter

from app.api.dependencies import CurrentUserDep
from app.schemas import UserResponseSchema

router = APIRouter(prefix="/users", tags=["users"])


@router.get(
    "/me",
    response_model=UserResponseSchema,
    summary="Get the currently authenticated user",
)
async def get_me(current_user: CurrentUserDep) -> UserResponseSchema:
    return UserResponseSchema(
        id=current_user.id,
        email=current_user.email,
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        is_active=current_user.is_active,
    )
