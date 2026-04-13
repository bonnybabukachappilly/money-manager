# app/api/v1/router/accounts.py
import logging


from app.api.dependencies import SessionDeps, AccountRepoDeps, CurrentUserDep
from fastapi import APIRouter, status, Request, HTTPException
from app.domain import Account
from app.schemas import CreditAccountCreate, CreditAccountResponse
from app.application.accounts import CreateNewAccount


router = APIRouter(prefix='/credit', tags=['accounts'])
log: logging.Logger = logging.getLogger(__name__)


@router.post(
    path='/new',
    response_model=CreditAccountResponse,
    status_code=status.HTTP_201_CREATED,
    summary='Create new credit account')
async def new_account(
        _: Request, body: CreditAccountCreate, session: SessionDeps,
        current_user: CurrentUserDep,
        account_repo: AccountRepoDeps) -> Account:

    use_case = CreateNewAccount(
        account_repo=account_repo,
        session=session
    )

    try:
        data = body.model_dump()
        data['user'] = current_user.id

        account: Account = await use_case.execute(data)

        await session.commit()

    except ValueError as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail='Unsupported Account type.'
        ) from e

    except Exception as e:
        await session.rollback()
        log.exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='unknown error occurred.'
        ) from e

    return account
