# app/application/user/login

from typing import Optional

from app.domain import User
from app.domain.repositories import UserRepository
from app.core.security import create_access_token, verify_password
from app.exceptions.application import (
    InvalidCredentialException, InactiveUserException
)


class LoginUser:
    def __init__(self, user_repo: UserRepository) -> None:
        self._repo: UserRepository = user_repo

    async def execute(self, email: str, password: str) -> str:
        user: Optional[User] = await self._repo.get_by_email(email)

        if user is None or not verify_password(password, user.hashed_password):
            raise InvalidCredentialException('Invalid email or password')

        if not user.is_active:
            raise InactiveUserException('This account has been deactivated')

        return create_access_token(subject=str(user.id))
