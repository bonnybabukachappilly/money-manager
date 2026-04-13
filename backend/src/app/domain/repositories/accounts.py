# app/domain/repositories/accounts.py

from abc import ABC, abstractmethod
from uuid import UUID
from typing import Optional
from app.domain import Account


class AccountRepository(ABC):
    @abstractmethod
    async def get_by_id(self, account_id: UUID) -> Optional[Account]:
        ...

    @abstractmethod
    async def get_by_user(self, user_id: UUID) -> list[Account]:
        ...

    @abstractmethod
    async def create(self, account: Account) -> None:
        ...

    @abstractmethod
    async def update(self, account: Account) -> None:
        ...

    @abstractmethod
    async def delete(self, account_id: UUID) -> None:
        ...

    @abstractmethod
    async def get_by_name(self, name: str, user: UUID) -> Optional[Account]:
        ...
