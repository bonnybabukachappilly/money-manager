# app/application/category/create.py


from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain import Category
from app.domain.repositories import CategoryRepository
from app.exceptions.database import (
    CategoryParentNotFoundException,
    NestedCategoryException, CategoryNotFoundException,
    CategoryUpdateException
)


class UpdateCategory:
    def __init__(
            self, category_repo: CategoryRepository,
            session: AsyncSession) -> None:
        self._repo: CategoryRepository = category_repo
        self._session: AsyncSession = session

    async def execute(self, data: dict, user: UUID) -> Category:
        category_id: UUID = data["id"]

        # 1. Fetch existing category
        category: Optional[Category] = await self._repo.get_by_id(
            user, category_id)

        if category is None:
            raise CategoryNotFoundException('Unable to find category')

        if "parent_name" in data and (_parent_name := data["parent_name"]):
            if _parent_name == 'null':
                category.parent_id = None
            else:
                _parent = await self._repo.get_by_name(user, _parent_name)

                if _parent is None:
                    raise CategoryParentNotFoundException(
                        "Specified parent not found.")

                if _parent.parent_id is not None:
                    raise NestedCategoryException(
                        "Nested categories are not allowed.")

                category.parent_id = _parent.id

        if "category_name" in data and data["category_name"]:
            category.category_name = data["category_name"]

        if "type" in data and data["type"]:
            category.type = data["type"]

        await self._repo.update(user, category)
        await self._session.flush()

        final_category = await self._repo.get_by_id(user, category_id)

        if final_category is None:
            raise CategoryUpdateException(
                'Failed to updated category')

        return final_category
