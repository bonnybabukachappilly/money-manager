# app/schemas/accounts.py
# pyright: reportIncompatibleVariableOverride=false

from datetime import datetime, date
from decimal import Decimal
from typing import Literal, Union, Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.domain.entities.accounts import AccountType


class AccountBaseSchema(BaseModel):
    """Shared fields for all account types."""
    account_name: str
    currency: str = "INR"
    balance: Decimal = Decimal("0.0")


class SavingsAccountCreate(AccountBaseSchema):
    type: Literal[AccountType.SAVINGS]


class WalletAccountCreate(AccountBaseSchema):
    type: Literal[AccountType.WALLET]


class CashAccountCreate(AccountBaseSchema):
    type: Literal[AccountType.CASH]


class CreditAccountCreate(AccountBaseSchema):
    type: Literal[AccountType.CREDIT]
    credit_limit: Decimal
    due_date: date


class LoanBaseCreate(AccountBaseSchema):
    loan_amount: Decimal
    installment_amount: Decimal
    total_installment: int
    interest_rate: Decimal
    installment_date: date


class LoanAccountCreate(LoanBaseCreate):
    type: Literal[AccountType.LOAN]


class EMIAccountCreate(LoanBaseCreate):
    type: Literal[AccountType.EMI]


class AccountResponse(AccountBaseSchema):
    """Common fields returned for any account."""
    id: UUID
    user: UUID
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SavingsAccountResponse(AccountResponse):
    type: Literal[AccountType.SAVINGS]


class WalletAccountResponse(AccountResponse):
    type: Literal[AccountType.WALLET]


class CashAccountResponse(AccountResponse):
    type: Literal[AccountType.CASH]


class CreditAccountResponse(AccountResponse):
    type: Literal[AccountType.CREDIT]
    credit_limit: Decimal
    billed_amount: Decimal
    unbilled_amount: Decimal
    due_date: date


class LoanBaseResponse(AccountResponse):
    """Shared logic for Loan/EMI response fields."""
    loan_amount: Decimal
    balance_amount: Decimal
    installment_amount: Decimal
    total_installment: int
    balance_installment: int
    interest_rate: Decimal
    installment_date: date


class LoanAccountResponse(LoanBaseResponse):
    type: Literal[AccountType.LOAN]


class EMIAccountResponse(LoanBaseResponse):
    type: Literal[AccountType.EMI]


GeneralCreateSchema = Annotated[
    Union[
        SavingsAccountCreate,
        CashAccountCreate,
        WalletAccountCreate
    ],
    Field(discriminator='type')
]

GeneralResponseSchema = Annotated[
    Union[
        SavingsAccountResponse,
        CashAccountResponse,
        WalletAccountResponse
    ],
    Field(discriminator='type')
]

RecurringCreateSchema = Annotated[
    Union[
        LoanAccountCreate,
        EMIAccountCreate
    ],
    Field(discriminator='type')
]

RecurringResponseSchema = Annotated[
    Union[
        LoanAccountResponse,
        EMIAccountResponse
    ],
    Field(discriminator='type')
]
