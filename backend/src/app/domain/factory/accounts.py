
from app.domain import (
    Account, SavingsAccount, CashAccount, WalletAccount,
    CreditAccount, LoanAccount, EMIAccount, AccountType
)

from app.db.models import (
    BaseAccountModel, SavingsAccountModel,
    CashAccountModel, WalletAccountModel,
    CreditAccountModel, LoanAccountModel,
    EMIAccountModel
)


from decimal import Decimal
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


class ToEntity:
    @staticmethod
    def to_entity(model: BaseAccountModel) -> Account:
        match model.type:
            case AccountType.SAVINGS:
                if isinstance(model, SavingsAccountModel):
                    return ToEntity._savings_entity(model)
                raise ValueError(
                    "Expected SavingsAccountModel for type SAVINGS")

            case AccountType.CASH:
                if isinstance(model, CashAccountModel):
                    return ToEntity._cash_entity(model)
                raise ValueError("Expected CashAccountModel for type CASH")

            case AccountType.WALLET:
                if isinstance(model, WalletAccountModel):
                    return ToEntity._wallet_entity(model)
                raise ValueError("Expected WalletAccountModel for type WALLET")

            case AccountType.CREDIT:
                if isinstance(model, CreditAccountModel):
                    return ToEntity._credit_entity(model)
                raise ValueError("Expected CreditAccountModel for type CREDIT")

            case AccountType.LOAN:
                if isinstance(model, LoanAccountModel):
                    return ToEntity._loan_entity(model)
                raise ValueError("Expected LoanAccountModel for type LOAN")

            case AccountType.EMI:
                if isinstance(model, EMIAccountModel):
                    return ToEntity._emi_entity(model)
                raise ValueError("Expected EMIAccountModel for type EMI")

            case _:
                raise ValueError(f"Unknown account type: {model.type}")

    @staticmethod
    def _get_base_args(model: BaseAccountModel) -> dict:
        return {
            "id": model.id,
            "user": model.user,
            "account_name": model.account_name,
            "currency": model.currency,
            "type": model.type,
            "balance": Decimal(str(model.balance)),
            "is_active": model.is_active,
            "created_at": model.created_at
        }

    @staticmethod
    def _savings_entity(model: BaseAccountModel) -> SavingsAccount:
        return SavingsAccount(**ToEntity._get_base_args(model))

    @staticmethod
    def _cash_entity(model: BaseAccountModel) -> CashAccount:
        return CashAccount(**ToEntity._get_base_args(model))

    @staticmethod
    def _wallet_entity(model: BaseAccountModel) -> WalletAccount:
        return WalletAccount(**ToEntity._get_base_args(model))

    @staticmethod
    def _credit_entity(model: CreditAccountModel) -> CreditAccount:
        return CreditAccount(
            **ToEntity._get_base_args(model),
            credit_limit=Decimal(str(model.credit_limit)),
            billed_amount=Decimal(str(model.billed_amount)),
            unbilled_amount=Decimal(str(model.unbilled_amount)),
            due_date=model.due_date
        )

    @staticmethod
    def _loan_entity(model: LoanAccountModel) -> LoanAccount:
        return LoanAccount(
            **ToEntity._get_base_args(model),
            loan_amount=Decimal(str(model.loan_amount)),
            balance_amount=Decimal(str(model.balance_amount)),
            installment_amount=Decimal(str(model.installment_amount)),
            total_installment=int(model.total_installment),
            balance_installment=int(model.balance_installment),
            interest_rate=Decimal(str(model.interest_rate)),
            installment_date=model.installment_date
        )

    @staticmethod
    def _emi_entity(model: LoanAccountModel) -> EMIAccount:
        return EMIAccount(
            **ToEntity._get_base_args(model),
            loan_amount=Decimal(str(model.loan_amount)),
            balance_amount=Decimal(str(model.balance_amount)),
            installment_amount=Decimal(str(model.installment_amount)),
            total_installment=int(model.total_installment),
            balance_installment=int(model.balance_installment),
            interest_rate=Decimal(str(model.interest_rate)),
            installment_date=model.installment_date
        )


class FromEntity:
    @staticmethod
    def to_model(entity: Account) -> BaseAccountModel:
        base_data = {
            "id": entity.id,
            "user": entity.user,
            "account_name": entity.account_name,
            "currency": entity.currency,
            "type": entity.type,
            "balance": Decimal(entity.balance),
            "is_active": entity.is_active,
            "created_at": entity.created_at
        }

        if isinstance(entity, CreditAccount):
            return CreditAccountModel(
                **base_data,
                credit_limit=Decimal(entity.credit_limit),
                billed_amount=Decimal(entity.billed_amount),
                unbilled_amount=Decimal(entity.unbilled_amount),
                due_date=entity.due_date
            )

        elif isinstance(entity, (LoanAccount, EMIAccount)):
            model_class = EMIAccountModel if isinstance(
                entity, EMIAccount) else LoanAccountModel

            return model_class(
                **base_data,
                loan_amount=Decimal(entity.loan_amount),
                balance_amount=Decimal(entity.balance_amount),
                installment_amount=Decimal(entity.installment_amount),
                total_installment=entity.total_installment,
                balance_installment=entity.balance_installment,
                interest_rate=float(entity.interest_rate),
                installment_date=entity.installment_date
            )

        elif isinstance(entity, SavingsAccount):
            return SavingsAccountModel(**base_data)

        elif isinstance(entity, CashAccount):
            return CashAccountModel(**base_data)

        elif isinstance(entity, WalletAccount):
            return WalletAccountModel(**base_data)

        return BaseAccountModel(**base_data)


class AccountFactory:
    @staticmethod
    def create_account(data: dict[str, Any]) -> Account:
        account_type = data.get("type")

        base_params = {
            "id": data.get("id") or uuid4(),
            "user": data.get("user"),
            "account_name": data.get("account_name"),
            "currency": data.get("currency", "INR"),
            "type": account_type,
            "balance": Decimal(str(data.get("balance", 0.0))),
            "is_active": data.get("is_active", True),
            "created_at": data.get("created_at") or datetime.now(timezone.utc)
        }

        match account_type:
            case AccountType.SAVINGS:
                return SavingsAccount(**base_params)

            case AccountType.CASH:
                return CashAccount(**base_params)

            case AccountType.WALLET:
                return WalletAccount(**base_params)

            case AccountType.CREDIT:
                return CreditAccount(
                    **base_params,
                    credit_limit=Decimal(str(data.get("credit_limit", 0.0))),
                    billed_amount=Decimal(str(data.get("billed_amount", 0.0))),
                    unbilled_amount=Decimal(
                        str(data.get("unbilled_amount", 0.0))),
                    due_date=data.get("due_date") or datetime.now(timezone.utc)
                )

            case AccountType.LOAN | AccountType.EMI:
                entity_class = (
                    EMIAccount if account_type == AccountType.EMI
                    else LoanAccount
                )

                return entity_class(
                    **base_params,
                    loan_amount=Decimal(str(data.get("loan_amount", 0.0))),
                    balance_amount=Decimal(
                        str(data.get("balance_amount", 0.0))),
                    installment_amount=Decimal(
                        str(data.get("installment_amount", 0.0))),
                    total_installment=int(data.get("total_installment", 0)),
                    balance_installment=int(
                        data.get("balance_installment", 0)),
                    interest_rate=Decimal(str(data.get("interest_rate", 0.0))),
                    installment_date=data.get(
                        "installment_date") or datetime.now(timezone.utc)
                )

            case _:
                raise ValueError(f"Unsupported account type: {account_type}")
