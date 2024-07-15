from __future__ import annotations
from typing import TYPE_CHECKING
from pydantic import BaseModel
from datetime import datetime

if TYPE_CHECKING:
    from firefly_report_bot.client.models.transactions import TransactionAttributes
    from firefly_report_bot.client.models.categories import CategoryEarned, CategorySpent, CategoryAttributes
    from firefly_report_bot.client.models.budgets import BudgetAttributes, BudgetLimitAttrebutes
    from firefly_report_bot.client.models.accounts import AccountAttributes


class Transaction(BaseModel):
    created_at: datetime | None = None
    budget_name: str | None = None
    category_name: str | None = None
    type: str | None = None
    amount: float = 0
    foreign_currency_code: str | None = None
    description: str | None = None
    source_name: str | None = None
    destination_name: str | None = None

    @classmethod
    def from_transaction_attributes(cls, transaction_attributes: TransactionAttributes) -> Transaction | None:
        """
        Generate a Transaction object from TransactionAttributes.

        Args:
            transaction_attributes (TransactionAttributes): The transaction attributes to create the Transaction from.

        Returns:
            Transaction | None: The created Transaction object or None if no transactions in the attributes.
        """

        if not transaction_attributes.transactions:
            return None
        transaction_split = transaction_attributes.transactions[0]
        return cls(
            created_at=transaction_attributes.created_at,
            budget_name=transaction_split.budget_name,
            category_name=transaction_split.category_name,
            type=transaction_split.type.value,
            amount=transaction_split.amount,
            foreign_currency_code=transaction_split.foreign_currency_code,
            description=transaction_split.description,
            source_name=transaction_split.source_name,
            destination_name=transaction_split.destination_name,
        )


class CategoryOperation(BaseModel):
    sum: float | None = None
    currency_code: str | None = None

    @classmethod
    def from_operation(cls, operation: CategoryEarned | CategorySpent) -> CategoryOperation:
        """
        Create a CategoryOperation object from a CategoryEarned or CategorySpent object.

        Args:
            operation (CategoryEarned | CategorySpent): The operation object to create the CategoryOperation from.

        Returns:
            CategoryOperation: The created CategoryOperation object.
        """
        return cls(sum=operation.sum, currency_code=operation.currency_code or "N/A")


class Category(BaseModel):
    name: str
    spent: CategoryOperation | None = None
    earned: CategoryOperation | None = None

    @classmethod
    def from_category_attributes(cls, category_attributes: CategoryAttributes) -> Category:
        """
        Create a Category object from the given CategoryAttributes.

        Args:
            category_attributes (CategoryAttributes): The attributes to create the Category object from.

        Returns:
            Category: The created Category object.
        """
        return cls(
            name=category_attributes.name,
            spent=(
                CategoryOperation.from_operation(category_attributes.spent[0]) if category_attributes.spent else None
            ),
            earned=(
                CategoryOperation.from_operation(category_attributes.earned[0]) if category_attributes.earned else None
            ),
        )


class BudgetOperation(BaseModel):
    pass


class Budget(BaseModel):
    name: str
    limit: float = 0
    limit_start: datetime | None
    limit_end: datetime | None
    limit_currency_code: str | None = None
    spent: float = 0

    @classmethod
    def from_budget_attributes(
        cls,
        budget_attributes: BudgetAttributes,
        budget_limit_attributes: BudgetLimitAttrebutes | None = None,
        budget_transactions: list[TransactionAttributes] | None = None,
    ) -> Budget:
        """
        Create a Budget object from the given
        BudgetAttributes, BudgetLimitAttributes, and list of TransactionAttributes.

        Args:
            budget_attributes (BudgetAttributes): The attributes to create the Budget object from.
            budget_limit_attributes (BudgetLimitAttrebutes, optional): The limit attributes for the budget. Defaults to None.
            budget_transactions (list[TransactionAttributes], optional): The list of transactions for the budget. Defaults to None.

        Returns:
            Budget: The created Budget object.
        """
        spent = 0.0
        for budget_transaction in budget_transactions or []:
            spent += budget_transaction.transactions[0].amount
        return cls(
            name=budget_attributes.name,
            limit=budget_limit_attributes.amount if budget_limit_attributes else 0,
            limit_start=budget_limit_attributes.start if budget_limit_attributes else None,
            limit_end=budget_limit_attributes.end if budget_limit_attributes else None,
            limit_currency_code=budget_limit_attributes.currency_code if budget_limit_attributes else None,
            spent=spent,
        )


class Account(BaseModel):
    name: str
    type: str
    current_balance: float
    currency_code: str | None = None

    @classmethod
    def from_account_attributes(cls, account_attributes: AccountAttributes) -> Account:
        """
        Creates an instance of the Account class from the given AccountAttributes.

        Args:
            account_attributes (AccountAttributes): The attributes of the account.

        Returns:
            Account: The created Account object.
        """
        return cls(
            name=account_attributes.name,
            type=account_attributes.type.value if account_attributes.type else "unknown",
            current_balance=account_attributes.current_balance or 0,
            currency_code=account_attributes.currency_code,
        )
