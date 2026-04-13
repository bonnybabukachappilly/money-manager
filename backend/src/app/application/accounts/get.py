# app/application/accounts/get.py


from typing import Optional
from uuid import UUID

from app.core.security import decode_token
from app.domain.repositories import AccountRepository
from app.domain import Account
from app.exceptions.database import AccountNotFoundException
from app.exceptions.application import InvalidTokenException


class GetAccountById:
    def __init__(self, repo: AccountRepository) -> None:
        self._repo: AccountRepository = repo

    async def execute(self, acc_id: UUID) -> Account:

        account: Optional[Account] = await self._repo.get_by_id(acc_id)

        if not account:
            raise AccountNotFoundException(
                f'Account with id {acc_id} not found.'
            )

        return account


class GetAccountByUser:
    def __init__(self, repo: AccountRepository) -> None:
        self._repo: AccountRepository = repo

    async def execute(self, token: str) -> list[Account]:
        try:
            payload = decode_token(token)
            user_id = UUID(payload["sub"])

        except (ValueError, KeyError) as e:
            raise InvalidTokenException('Token invalid or expired') from e

        return await self._repo.get_by_user(user_id)
