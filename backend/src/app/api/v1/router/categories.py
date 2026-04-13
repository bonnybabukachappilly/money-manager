# app/api/v1/router/categories.py
import logging
from uuid import UUID

from fastapi import APIRouter, status, Request, HTTPException


from app.api.dependencies import SessionDeps, CategoryRepoDeps, CurrentUserDep
from app.domain import Category
from app.schemas import (
    CategoryCreateSchema, CategoryResponseSchema,
    CategoryGetSchema, CategoryUpdateSchema
)
from app.exceptions.database import (
    CategoryNameExistsException,
    CategoryParentNotFoundException,
    NestedCategoryException, CategoryUpdateException,
    CategoryNotFoundException, CategoryCreateException
)

from app.application.category import (
    CreateNewCategory, GetAllCategory,
    GetCategoryById, GetAllRootCategory,
    GetSubCategory, UpdateCategory, DeleteCategory
)


router = APIRouter(prefix='/categories', tags=['accounts'])
log: logging.Logger = logging.getLogger(__name__)


@router.post(
    path='/new',
    response_model=CategoryResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary='Create new Category [expense | Income]')
async def new_account(
        _: Request, body: CategoryCreateSchema, session: SessionDeps,
        current_user: CurrentUserDep,
        category_repo: CategoryRepoDeps) -> Category:

    use_case = CreateNewCategory(
        category_repo=category_repo,
        session=session
    )

    try:
        category: Category = await use_case.execute(
            data=body.model_dump(),
            user=current_user.id
        )

        await session.commit()

    except CategoryNameExistsException as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Category name already exists.'
        ) from e

    except CategoryParentNotFoundException as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Unable to find parent.'
        ) from e

    except CategoryCreateException as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Failed to create category.'
        ) from e

    except NestedCategoryException as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                'Nesting category is not allowed,' +
                'Parent should not have other parent.'
            )
        ) from e

    except Exception as e:
        await session.rollback()
        log.exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='unknown error occurred.'
        ) from e

    return category


@router.get(
    path='/',
    response_model=list[CategoryResponseSchema],
    status_code=status.HTTP_200_OK,
    summary='Get all categories')
async def get_all_category(
        current_user: CurrentUserDep,
        category_repo: CategoryRepoDeps) -> list[Category]:
    use_case = GetAllCategory(category_repo)

    try:
        categories: list[Category] = await use_case.execute(current_user.id)

    except CategoryNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Category not found.'
        ) from e

    return categories


@router.get(
    path='/id',
    response_model=CategoryResponseSchema,
    status_code=status.HTTP_200_OK,
    summary='Get category by id')
async def get_category_by_id(
        current_user: CurrentUserDep, category_id: CategoryGetSchema,
        category_repo: CategoryRepoDeps) -> Category:
    use_case = GetCategoryById(category_repo)

    try:
        categories: Category = await use_case.execute(
            user_id=current_user.id,
            cat_id=category_id.id
        )

    except CategoryNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Category not found.'
        ) from e

    return categories


@router.get(
    path='/root',
    response_model=list[CategoryResponseSchema],
    status_code=status.HTTP_200_OK,
    summary='Get all root categories')
async def get_all_root_category(
        current_user: CurrentUserDep,
        category_repo: CategoryRepoDeps) -> list[Category]:
    use_case = GetAllRootCategory(category_repo)

    try:
        categories: list[Category] = await use_case.execute(current_user.id)

    except CategoryNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Category not found.'
        ) from e

    return categories


@router.get(
    path='/sub',
    response_model=list[CategoryResponseSchema],
    status_code=status.HTTP_200_OK,
    summary='Get all sub categories')
async def get_all_sub_category(
        current_user: CurrentUserDep, category_id: CategoryGetSchema,
        category_repo: CategoryRepoDeps) -> list[Category]:
    use_case = GetSubCategory(category_repo)

    try:
        categories: list[Category] = await use_case.execute(
            user_id=current_user.id,
            parent=category_id.id
        )

    except CategoryNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Category not found.'
        ) from e

    return categories


@router.patch(
    path='/update',
    response_model=CategoryResponseSchema,
    status_code=status.HTTP_200_OK,
    summary='Update existing category')
async def update_account(
        _: Request, body: CategoryUpdateSchema, session: SessionDeps,
        current_user: CurrentUserDep,
        category_repo: CategoryRepoDeps) -> Category:

    use_case = UpdateCategory(
        category_repo=category_repo,
        session=session
    )

    try:
        category: Category = await use_case.execute(
            data=body.model_dump(),
            user=current_user.id
        )

        await session.commit()

    except CategoryNotFoundException as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Category not found.'
        ) from e

    except CategoryParentNotFoundException as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Unable to find parent.'
        ) from e

    except NestedCategoryException as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                'Nesting category is not allowed,' +
                'Parent should not have other parent.'
            )
        ) from e

    except CategoryUpdateException as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Failed to updated category.'
        ) from e

    except Exception as e:
        await session.rollback()
        log.exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='unknown error occurred.'
        ) from e

    return category


@router.delete(
    path='/delete',
    status_code=status.HTTP_200_OK,
    summary='Delete category')
async def delete_category(
        current_user: CurrentUserDep, category_id: CategoryGetSchema,
        session: SessionDeps,
        category_repo: CategoryRepoDeps) -> None:

    use_case = DeleteCategory(category_repo=category_repo, session=session)

    try:
        await use_case.execute(
            user_id=current_user.id,
            category_id=category_id.id
        )

        await session.commit()

    except CategoryNotFoundException as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Category not found.'
        ) from e

    except NestedCategoryException as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                'Nesting category is not allowed,' +
                'Parent should not have other parent.'
            )
        ) from e

    return None
