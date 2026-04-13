# app/domain/repositories/user.py

from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID
from app.domain import User


class UserRepository(ABC):
    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        ...

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        ...

    @abstractmethod
    async def create(self, user: User) -> None:
        ...

    @abstractmethod
    async def update(self, user: User) -> None:
        ...

    @abstractmethod
    async def delete(self, user_id: UUID) -> None:
        ...
