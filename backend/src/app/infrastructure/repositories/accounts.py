# app/infrastructure/repositories/accounts.py

from app.domain import Account
from uuid import UUID
from typing import Optional, Sequence, Tuple, cast

from sqlalchemy import Result, Select, Delete, select, delete as sql_delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.domain.repositories import AccountRepository
from app.exceptions.database import AccountNotFoundException
from app.domain.factory import ToEntity, FromEntity

from app.db.models import (
    BaseAccountModel, EMIAccountModel,
    CreditAccountModel, LoanAccountModel,
)


class SQLAccountRepository(AccountRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session: AsyncSession = session

    async def get_by_id(self, account_id: UUID) -> Optional[Account]:
        model: Optional[BaseAccountModel] = await self._session.get(
            BaseAccountModel, account_id
        )

        return None if model is None else ToEntity.to_entity(model)

    async def get_by_user(self, user_id: UUID) -> list[Account]:
        stmt: Select[tuple[BaseAccountModel]] = (
            select(BaseAccountModel)
            .options(joinedload(BaseAccountModel.user_relationship))
            .where(BaseAccountModel.user == user_id)
            .order_by(BaseAccountModel.created_at)
        )

        results: Result[tuple[BaseAccountModel]] = await self._session.execute(
            stmt)

        models: Sequence[BaseAccountModel] = results.scalars().all()

        return cast(list[Account], [ToEntity.to_entity(m) for m in models])

    async def create(self, account: Account) -> None:
        db_model: BaseAccountModel = FromEntity.to_model(account)
        self._session.add(db_model)

    async def update(self, account: Account) -> None:
        model: Optional[BaseAccountModel] = await self._session.get(
            BaseAccountModel, account.id
        )

        if not model:
            raise AccountNotFoundException(
                f"Account with id {account.id} not found")

        updated_data: BaseAccountModel = FromEntity.to_model(account)

        model.account_name = updated_data.account_name
        model.is_active = updated_data.is_active
        model.currency = updated_data.currency

        if (isinstance(model, CreditAccountModel)
                and isinstance(updated_data, CreditAccountModel)):
            model.credit_limit = updated_data.credit_limit
            model.billed_amount = updated_data.billed_amount
            model.unbilled_amount = updated_data.unbilled_amount
            model.due_date = updated_data.due_date

        elif ((
            isinstance(model, LoanAccountModel)
            and isinstance(updated_data, LoanAccountModel)
        ) or (
            isinstance(model, EMIAccountModel)
            and isinstance(updated_data, EMIAccountModel)
        )):

            model.balance_amount = updated_data.balance_amount
            model.balance_installment = updated_data.balance_installment
            model.installment_date = updated_data.installment_date

    async def get_by_name(self, name: str, user: UUID) -> Optional[Account]:
        stmt: Select[Tuple[BaseAccountModel]] = select(
            BaseAccountModel).where(
                func.lower(BaseAccountModel.account_name) == func.lower(name),
                BaseAccountModel.user == user
        )

        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()

        return None if model is None else ToEntity.to_entity(model)

    async def delete(self, account_id: UUID) -> None:
        stmt: Delete = sql_delete(BaseAccountModel).where(
            BaseAccountModel.id == account_id)

        await self._session.execute(stmt)
