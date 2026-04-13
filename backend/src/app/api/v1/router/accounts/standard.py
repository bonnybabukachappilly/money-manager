# app/api/v1/router/accounts.py
import logging

from fastapi import APIRouter, status, Request, HTTPException
from app.api.dependencies import SessionDeps, AccountRepoDeps, CurrentUserDep
from app.domain import Account
from app.schemas import GeneralCreateSchema, GeneralResponseSchema
from app.exceptions.database import AccountNameExistsException

from app.application.accounts import CreateNewAccount


router = APIRouter(prefix='/standard', tags=['accounts'])
log: logging.Logger = logging.getLogger(__name__)


@router.post(
    path='/new',
    response_model=GeneralResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary='Create new standard account [Savings | Cash  | Wallet]')
async def new_account(
        _: Request, body: GeneralCreateSchema, session: SessionDeps,
        current_user: CurrentUserDep,
        account_repo: AccountRepoDeps) -> Account:

    use_case = CreateNewAccount(
        account_repo=account_repo,
        session=session
    )

    try:
        account: Account = await use_case.execute(
            data=body.model_dump(),
            user=current_user.id
        )

        await session.commit()

    except ValueError as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail='Unsupported Account type.'
        ) from e

    except AccountNameExistsException as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Account name already exists.'
        ) from e

    except Exception as e:
        await session.rollback()
        log.exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='unknown error occurred.'
        ) from e

    return account
