# app/infrastructure/repositories/user.py

from typing import Optional

from uuid import UUID
from app.domain import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Select, Result, Delete, select, delete as sql_delete
from app.domain.repositories import UserRepository

from app.db.models import UserModel
from app.exceptions.database import UserNotFoundException


class SQLUserRepository(UserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session: AsyncSession = session

    def _to_entity(self, model: Optional[UserModel]) -> Optional[User]:
        if model is None:
            return None

        return User(
            id=model.id,
            first_name=model.first_name,
            last_name=model.last_name,
            email=model.email,
            hashed_password=model.hashed_password,
            is_active=model.is_active
        )

    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        model: Optional[UserModel] = await self._session.get(
            UserModel, user_id)

        return self._to_entity(model)

    async def get_by_email(self, email: str) -> Optional[User]:
        stmt: Select[tuple[UserModel]] = select(
            UserModel).where(UserModel.email == email)

        result: Result[tuple[UserModel]] = await self._session.execute(stmt)

        return self._to_entity(result.scalar_one_or_none())

    async def create(self, user: User) -> None:
        model = UserModel(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            hashed_password=user.hashed_password,
            is_active=user.is_active
        )

        self._session.add(model)

    async def update(self, user: User) -> None:
        model: Optional[UserModel] = await self._session.get(
            UserModel, user.id)

        if model is None:
            raise UserNotFoundException('Unable to find the user.')

        model.first_name = user.first_name
        model.last_name = user.last_name
        model.email = user.email
        model.hashed_password = user.hashed_password
        model.is_active = user.is_active

    async def delete(self, user_id: UUID) -> None:
        stmt: Delete = sql_delete(UserModel).where(UserModel.id == user_id)
        await self._session.execute(stmt)
