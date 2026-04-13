# app/domain/entities/accounts.py

from dataclasses import dataclass
from uuid import UUID
from datetime import datetime, date
from enum import Enum
from decimal import Decimal


class AccountType(str, Enum):
    SAVINGS = "savings"
    CREDIT = "credit"
    CASH = "cash"
    EMI = "emi"
    LOAN = "loan"
    WALLET = "wallet"


@dataclass
class Account:
    id: UUID
    user: UUID
    account_name: str
    currency: str
    type: AccountType
    balance: Decimal
    is_active: bool
    created_at: datetime


@dataclass
class SavingsAccount(Account):
    pass


@dataclass
class CashAccount(Account):
    pass


@dataclass
class WalletAccount(Account):
    pass


@dataclass
class CreditAccount(Account):
    credit_limit: Decimal
    billed_amount: Decimal
    unbilled_amount: Decimal
    due_date: date


@dataclass
class LoanAccount(Account):
    loan_amount: Decimal
    balance_amount: Decimal
    installment_amount: Decimal
    total_installment: int
    balance_installment: int
    interest_rate: Decimal
    installment_date: date


@dataclass
class EMIAccount(LoanAccount):
    pass
