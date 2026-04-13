# app/application/category/get.py

from typing import Optional
from uuid import UUID

from app.domain.repositories import CategoryRepository
from app.domain import Category
from app.exceptions.database import CategoryNotFoundException


class GetCategoryById:
    def __init__(self, repo: CategoryRepository) -> None:
        self._repo: CategoryRepository = repo

    async def execute(self, user_id: UUID, cat_id: UUID) -> Category:
        category: Optional[Category] = await self._repo.get_by_id(
            user_id, cat_id)

        if not category:
            raise CategoryNotFoundException(
                f'Category with id {cat_id}'
            )

        return category


class GetAllCategory:
    def __init__(self, repo: CategoryRepository) -> None:
        self._repo: CategoryRepository = repo

    async def execute(self, user_id: UUID) -> list[Category]:
        category: list[Category] = await self._repo.get_all(user_id)

        if not category:
            raise CategoryNotFoundException(
                'No Category found for current user. '
            )

        return category


class GetAllRootCategory:
    def __init__(self, repo: CategoryRepository) -> None:
        self._repo: CategoryRepository = repo

    async def execute(self, user_id: UUID) -> list[Category]:
        category: list[Category] = await self._repo.get_root_categories(
            user_id)

        if not category:
            raise CategoryNotFoundException(
                'No Category found for current user. '
            )

        return category


class GetSubCategory:
    def __init__(self, repo: CategoryRepository) -> None:
        self._repo: CategoryRepository = repo

    async def execute(self, user_id: UUID, parent: UUID) -> list[Category]:
        category: list[Category] = await self._repo.get_subcategories(
            user_id, parent)

        if not category:
            raise CategoryNotFoundException(
                f'Category with id {parent}'
            )

        return category
