# app/infrastructure/repositories/categories.py

from uuid import UUID
from typing import Optional, Sequence

from sqlalchemy import Result, Select, Delete, select, delete as sql_delete, inspect
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import CategoryModel
from app.domain import Category
from app.domain.repositories import CategoryRepository

from app.exceptions.database import CategoryNotFoundException


class SQLCategoryRepository(CategoryRepository):

    def __init__(self, session: AsyncSession) -> None:
        self._session: AsyncSession = session

    def _to_entity(
            self, model: Optional[CategoryModel]) -> Optional[Category]:
        if model is None:
            return None

        parent_name: Optional[str] = None

        # inst = inspect(model)

        if model.parent_id is not None:
            # if "parent_relationship" in inst.unloaded:
            #     parent_name = None
            if hasattr(model, "parent_relationship") and model.parent_relationship:
                parent_name = model.parent_relationship.category_name

        return Category(
            id=model.id,
            user=model.user,
            category_name=model.category_name,
            type=model.type,
            parent_id=model.parent_id,
            parent_name=parent_name,
            created_at=model.created_at
        )

    async def get_by_id(
            self, user_id: UUID, category_id: UUID) -> Optional[Category]:

        stmt: Select[tuple[CategoryModel]] = (
            select(CategoryModel)
            .options(joinedload(CategoryModel.parent_relationship))
            .where(
                CategoryModel.id == category_id,
                CategoryModel.user == user_id
            )
        )

        results: Result[tuple[CategoryModel]] = await self._session.execute(
            stmt
        )

        model: Optional[CategoryModel] = results.scalar_one_or_none()

        return self._to_entity(model)

    async def get_by_name(
            self, user_id: UUID, name: str) -> Optional[Category]:
        stmt: Select[tuple[CategoryModel]] = (
            select(CategoryModel)
            .options(joinedload(CategoryModel.parent_relationship))
            .where(
                CategoryModel.category_name == name,
                CategoryModel.user == user_id
            )
        )

        results: Result[tuple[CategoryModel]] = await self._session.execute(
            stmt
        )

        model: Optional[CategoryModel] = results.scalar_one_or_none()

        return self._to_entity(model)

    async def get_all(
            self, user_id: UUID) -> list[Category]:
        stmt: Select[tuple[CategoryModel]] = (
            select(CategoryModel)
            .where(CategoryModel.user == user_id)
            .order_by(CategoryModel.category_name)
        )

        results: Result[tuple[CategoryModel]] = await self._session.execute(
            stmt
        )

        models: Sequence[CategoryModel] = results.scalars().all()

        return [
            entity for m in models if (
                entity := self._to_entity(m)) is not None]

    async def get_root_categories(
            self, user_id: UUID) -> list[Category]:
        stmt: Select[tuple[CategoryModel]] = (
            select(CategoryModel)
            .where(
                CategoryModel.user == user_id,
                CategoryModel.parent_id.is_(None)
            )
            .order_by(CategoryModel.category_name)
        )

        results: Result[tuple[CategoryModel]] = await self._session.execute(
            stmt
        )

        models: Sequence[CategoryModel] = results.scalars().all()

        return [
            entity for m in models if (
                entity := self._to_entity(m)) is not None]

    async def get_subcategories(
            self, user_id: UUID, parent: UUID) -> list[Category]:
        stmt: Select[tuple[CategoryModel]] = (
            select(CategoryModel)
            .options(joinedload(CategoryModel.parent_relationship))
            .where(
                CategoryModel.user == user_id,
                CategoryModel.parent_id == parent
            )
            .order_by(CategoryModel.category_name)
        )

        results: Result[tuple[CategoryModel]] = await self._session.execute(
            stmt
        )

        models: Sequence[CategoryModel] = results.scalars().all()

        return [
            entity for m in models if (
                entity := self._to_entity(m)) is not None]

    async def create(
            self, user_id: UUID, category: Category) -> None:
        db_model: CategoryModel = CategoryModel(
            id=category.id,
            user=category.user,
            category_name=category.category_name,
            type=category.type,
            parent_id=category.parent_id,
            created_at=category.created_at
        )

        self._session.add(db_model)

    async def update(
            self, user_id: UUID, category: Category) -> None:
        model: Optional[CategoryModel] = await self._session.get(
            CategoryModel, category.id)

        if model is None or model.user != user_id:
            raise CategoryNotFoundException(
                'Category not found or access denied.')

        model.category_name = category.category_name
        model.type = category.type
        model.parent_id = category.parent_id

    async def delete(
            self, user_id: UUID, category_id: UUID) -> None:
        stmt: Delete = sql_delete(CategoryModel).where(
            CategoryModel.user == user_id,
            CategoryModel.id == category_id
        )
        await self._session.execute(stmt)
