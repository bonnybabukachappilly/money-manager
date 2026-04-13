# app/domain/repositories/Category.py

from abc import ABC, abstractmethod
from uuid import UUID
from typing import Optional
from app.domain import Category


class CategoryRepository(ABC):
    @abstractmethod
    async def get_by_id(
            self, user_id: UUID, category_id: UUID) -> Optional[Category]:
        ...

    @abstractmethod
    async def get_by_name(
            self, user_id: UUID, name: str) -> Optional[Category]:
        ...

    @abstractmethod
    async def get_all(
            self, user_id: UUID) -> list[Category]:
        ...

    @abstractmethod
    async def get_root_categories(
            self, user_id: UUID) -> list[Category]:
        ...

    @abstractmethod
    async def get_subcategories(
            self, user_id: UUID, parent: UUID) -> list[Category]:
        ...

    @abstractmethod
    async def create(
            self, user_id: UUID, category: Category) -> None:
        ...

    @abstractmethod
    async def update(
            self, user_id: UUID, category: Category) -> None:
        ...

    @abstractmethod
    async def delete(
            self, user_id: UUID, category_id: UUID) -> None:
        ...
