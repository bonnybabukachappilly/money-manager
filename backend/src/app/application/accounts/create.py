# app/application/accounts/create.py

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain import Account
from app.domain.repositories import AccountRepository
from app.domain.factory import AccountFactory
from app.exceptions.database import AccountNameExistsException


class CreateNewAccount:
    def __init__(
            self, account_repo: AccountRepository,
            session: AsyncSession) -> None:
        self._repo: AccountRepository = account_repo
        self._session: AsyncSession = session

    async def execute(self, data: dict, user: UUID) -> Account:
        _name: str = data["account_name"]

        _account: Account | None = await self._repo.get_by_name(_name, user)

        if _account is not None:
            raise AccountNameExistsException('Account name already exists.')

        entity: Account = AccountFactory.create_account(data)

        await self._repo.create(entity)
        await self._session.flush()

        return entity
