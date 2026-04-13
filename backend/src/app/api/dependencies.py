# app/api/dependencies.py
from typing import AsyncGenerator, Annotated

from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db_session
from app.domain import User
from app.application.user import GetCurrentUser
from app.infrastructure.repositories import (
    SQLUserRepository, SQLAccountRepository
)
from fastapi import Depends, HTTPException, status
from app.exceptions.application import (
    InvalidTokenException,
    InactiveUserException
)
from app.exceptions.database import UserNotFoundException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


# ---------- Session dependency ----------
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async for session in get_db_session():
        yield session


SessionDeps = Annotated[AsyncSession, Depends(get_session)]


# ---------- Repository dependencies ----------

def get_user_repository(session: SessionDeps) -> SQLUserRepository:
    return SQLUserRepository(session)


def get_account_repository(session: SessionDeps) -> SQLAccountRepository:
    return SQLAccountRepository(session)


UserRepoDeps = Annotated[
    SQLUserRepository,
    Depends(get_user_repository)]

AccountRepoDeps = Annotated[
    SQLAccountRepository,
    Depends(get_account_repository)]


# ---------- Auth dependency ----------
async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        repo: UserRepoDeps) -> User:
    use_case = GetCurrentUser(repo)

    try:
        return await use_case.execute(token)

    except (InvalidTokenException, UserNotFoundException) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED
        ) from e

    except InactiveUserException as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This account has been deactivated.",
        ) from e


CurrentUserDep = Annotated[User, Depends(get_current_user)]
