# app/application/user/register

from typing import Optional
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.repositories import UserRepository
from app.domain import User
from app.exceptions.application import EmailAlreadyExistsError
from app.core.security import hash_password


class RegisterUser:
    def __init__(
            self, user_repo: UserRepository, session: AsyncSession) -> None:
        self._repo: UserRepository = user_repo
        self._session: AsyncSession = session

    async def execute(
            self, fname: str, lname: str, email: str, password: str) -> User:
        exist: Optional[User] = await self._repo.get_by_email(email)

        if exist:
            raise EmailAlreadyExistsError(f'User with {email} already exists.')

        user = User(
            id=uuid4(),
            first_name=fname,
            last_name=lname,
            email=email,
            hashed_password=hash_password(password)
        )

        await self._repo.create(user)
        await self._session.flush()

        return user
