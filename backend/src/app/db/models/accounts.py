# app/db/models/accounts.py

from typing import Any, TYPE_CHECKING
from datetime import datetime, timezone, date

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    String, ForeignKey, Boolean,
    Numeric, DateTime, Date,
    Enum as SQLEnum
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from uuid import UUID, uuid4

from app.db import Base
from app.domain import AccountType

if TYPE_CHECKING:
    from .user import UserModel


class BaseAccountModel(Base):
    __tablename__: Any = 'accounts'

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )

    user: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )

    account_name: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True
    )

    currency: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        default="INR",
    )

    type: Mapped[AccountType] = mapped_column(
        SQLEnum(AccountType),
        nullable=False,
        default=AccountType.SAVINGS
    )

    balance: Mapped[float] = mapped_column(
        Numeric(15, 2),
        nullable=False,
        default=0.00,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    user_relationship: Mapped['UserModel'] = relationship(
        'UserModel',
        lazy='raise'
    )

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'base_account'
    }


class SavingsAccountModel(BaseAccountModel):
    __tablename__ = None
    __mapper_args__ = {'polymorphic_identity': AccountType.SAVINGS}


class CashAccountModel(BaseAccountModel):
    __tablename__ = None
    __mapper_args__ = {'polymorphic_identity': AccountType.CASH}


class WalletAccountModel(BaseAccountModel):
    __tablename__ = None
    __mapper_args__ = {'polymorphic_identity': AccountType.WALLET}


class CreditAccountModel(BaseAccountModel):
    __tablename__ = 'credit_accounts'

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey('accounts.id', ondelete='CASCADE'),
        primary_key=True
    )

    credit_limit: Mapped[float] = mapped_column(
        Numeric(15, 2),
        nullable=False,
        default=0.00,
    )

    billed_amount: Mapped[float] = mapped_column(
        Numeric(15, 2),
        nullable=False,
        default=0.00,
    )

    unbilled_amount: Mapped[float] = mapped_column(
        Numeric(15, 2),
        nullable=False,
        default=0.00,
    )

    due_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        default=lambda: date.today,
    )

    __mapper_args__ = {"polymorphic_identity": AccountType.CREDIT}


class LoanAccountModel(BaseAccountModel):
    __tablename__ = 'loan_accounts'

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey('accounts.id', ondelete='CASCADE'),
        primary_key=True
    )

    loan_amount: Mapped[float] = mapped_column(
        Numeric(15, 2),
        nullable=False,
        default=0.00,
    )

    balance_amount: Mapped[float] = mapped_column(
        Numeric(15, 2),
        nullable=False,
        default=0.00,
    )

    installment_amount: Mapped[float] = mapped_column(
        Numeric(15, 2),
        nullable=False,
        default=0.00,
    )

    total_installment: Mapped[float] = mapped_column(
        Numeric(15, 0),
        nullable=False,
        default=0,
    )

    balance_installment: Mapped[float] = mapped_column(
        Numeric(15, 0),
        nullable=False,
        default=0,
    )

    interest_rate: Mapped[float] = mapped_column(
        Numeric(5, 2),
        nullable=False,
        default=0.00,
    )

    installment_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        default=lambda: date.today,
    )

    __mapper_args__ = {"polymorphic_identity": AccountType.LOAN}


class EMIAccountModel(LoanAccountModel):
    __tablename__ = None
    __mapper_args__ = {"polymorphic_identity": AccountType.EMI}
