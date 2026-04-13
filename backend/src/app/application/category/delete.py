# app/application/category/delete.py

from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.repositories import CategoryRepository
from app.exceptions.database import (
    CategoryNotFoundException, CategoryInUseException
)


class DeleteCategory:
    def __init__(
            self, category_repo: CategoryRepository,
            session: AsyncSession) -> None:
        self._repo: CategoryRepository = category_repo
        self._session: AsyncSession = session

    async def execute(self, user_id: UUID, category_id: UUID) -> None:
        category = await self._repo.get_by_id(user_id, category_id)

        if not category:
            raise CategoryNotFoundException(
                "Category not found or access denied.")

        subcategories = await self._repo.get_subcategories(
            user_id, category_id)

        if subcategories:
            raise CategoryInUseException(
                "Cannot delete a category that has subcategories. " +
                "Move or delete them first."
            )

        await self._repo.delete(user_id, category_id)
        await self._session.flush()
