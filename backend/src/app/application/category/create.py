# app/application/category/create.py


from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain import Category
from app.domain.repositories import CategoryRepository
from app.exceptions.database import (
    CategoryNameExistsException, CategoryParentNotFoundException,
    NestedCategoryException, CategoryCreateException
)


class CreateNewCategory:
    def __init__(
            self, category_repo: CategoryRepository,
            session: AsyncSession) -> None:
        self._repo: CategoryRepository = category_repo
        self._session: AsyncSession = session

    async def execute(self, data: dict, user: UUID) -> Category:
        _name: str = data["category_name"]

        _category: Optional[Category] = await self._repo.get_by_name(
            user, _name,)

        if _category is not None:
            raise CategoryNameExistsException('Category name already exists.')

        _parent_name: Optional[str] = data.get('parent_name')
        _parent_id: Optional[UUID] = None

        if _parent_name is not None:
            _parent: Optional[Category] = await self._repo.get_by_name(
                user, _parent_name)

            if _parent is None:
                raise CategoryParentNotFoundException(
                    "Unable to find specified parent."
                )

            if _parent.parent_id is not None:
                raise NestedCategoryException(
                    "Nested category not allowed."
                )

            _parent_id = _parent.id

        entity: Category = Category(
            id=uuid4(),
            user=user,
            category_name=data['category_name'],
            type=data['type'],
            parent_id=_parent_id,
            created_at=data.get("created_at") or datetime.now(timezone.utc)
        )

        await self._repo.create(user, entity)
        await self._session.flush()

        final_category = await self._repo.get_by_id(user, entity.id)

        if final_category is None:
            raise CategoryCreateException(
                'Failed to create category')

        return entity
