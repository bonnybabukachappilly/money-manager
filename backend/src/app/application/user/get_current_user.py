# app/application/user/get_current_user.py

from typing import Any, Optional
from uuid import UUID

from app.core.security import decode_token
from app.domain import User
from app.domain.repositories import UserRepository
from app.exceptions.application import (
    InvalidTokenException,
    InactiveUserException
)
from app.exceptions.database import UserNotFoundException


class GetCurrentUser:
    def __init__(self, repo: UserRepository) -> None:
        self._repo: UserRepository = repo

    async def execute(self, token: str) -> User:
        try:
            payload: dict[str, Any] = decode_token(token)
            user_id = UUID(payload["sub"])

        except (ValueError, KeyError) as e:
            raise InvalidTokenException('Token invalid or expired') from e

        user: Optional[User] = await self._repo.get_by_id(user_id)

        if user is None:
            raise UserNotFoundException('User not found')

        if not user.is_active:
            InactiveUserException('This account have been deactivated')

        return user
