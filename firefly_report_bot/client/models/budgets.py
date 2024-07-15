from datetime import datetime
from pydantic import Field, BaseModel

from firefly_report_bot.client.models.base import BaseAttributes, BaseFireflyModel, BaseData
from firefly_report_bot.client.enums import AutoBudgetPeriod, AutoBudgetType
from firefly_report_bot.client.models.transactions import TransactionAttributes


class BudgetSpent(BaseModel):
    """
    Represents the amount of money spent on a budget.

    Attributes:
        sum (float or None): The amount of money spent.
        currency_id (str or None): The ID of the currency.
        currency_code (str or None): The code of the currency.
        currency_symbol (str or None): The symbol of the currency.
        currency_decimal_places (int or None): The number of decimal places for the currency.
    """

    sum: float | None = None
    currency_id: int | str | None = None
    currency_code: str | None = None
    currency_symbol: str | None = None
    currency_decimal_places: int | None = None


class BudgetAttributes(BaseAttributes):
    """
    Represents the attributes of a budget.

    Attributes:
        created_at (datetime or None): The datetime when the budget was created.
        updated_at (datetime or None): The datetime when the budget was last updated.
        name (str): The name of the budget.
        active (bool or None): Flag indicating if the budget is active.
        notes (str or None): Additional notes for the budget.
        order (int or None): The order of the budget.
        auto_budget_type (AutoBudgetType or None): The type of auto budget.
        auto_budget_currency_id (str or None): The ID of the auto budget currency.
        auto_budget_currency_code (str or None): The code of the auto budget currency.
        auto_budget_amount (float or None): The amount of the auto budget.
        auto_budget_period (AutoBudgetPeriod or None): The period of the auto budget.
        spent (list[BudgetSpent]): The list of amounts spent on the budget.
    """

    created_at: datetime | None = None
    updated_at: datetime | None = None
    name: str
    active: bool | None = None
    notes: str | None = None
    order: int | None = None
    auto_budget_type: AutoBudgetType | None = Field(None)
    auto_budget_currency_id: int | None = None
    auto_budget_currency_code: str | None = None
    auto_budget_amount: float | None = None
    auto_budget_period: AutoBudgetPeriod | None = Field(None)
    spent: list[BudgetSpent] = Field(..., default_factory=list)


class BudgetData(BaseData):
    """
    Class representing the data of a budget.

    Attributes:
        attributes (BudgetAttributes): The attributes of the budget.
    """

    attributes: BudgetAttributes


class BudgetModel(BaseFireflyModel):
    """
    Represents a budget returned by the API.

    Attributes:
        data (BudgetData): The data of the budget.
    """

    data: BudgetData


class BudgetsModel(BaseFireflyModel):
    """
    Represents a collection of budgets returned by the API.

    Attributes:
        data (list[BudgetData]): A list of BudgetData objects representing the budgets returned by the API.
    """

    data: list[BudgetData]


class BudgetLimitAttrebutes(BaseAttributes):
    """
    Represents the attributes of a budget limit.

    Attributes:
        created_at (datetime or None): The datetime when the budget limit was created.
        updated_at (datetime or None): The datetime when the budget limit was last updated.
        start (datetime): The start datetime of the budget limit.
        end (datetime): The end datetime of the budget limit.
        currency_id (int or str or None): The ID of the currency.
        currency_code (str or None): The code of the currency.
        currency_name (str or None): The name of the currency.
        currency_symbol (str or None): The symbol of the currency.
        currency_decimal_places (int or None): The number of decimal places for the currency.
        budget_id (int): The ID of the budget.
        period (str or None): The period of the budget limit.
        amount (float): The amount of the budget limit.
        spent (float): The amount of money spent on the budget limit.
    """

    created_at: datetime | None = None
    updated_at: datetime | None = None
    start: datetime
    end: datetime
    currency_id: int | str | None = None
    currency_code: str | None = None
    currency_name: str | None = None
    currency_symbol: str | None = None
    currency_decimal_places: int | None = None
    budget_id: int
    period: str | None = None
    amount: float
    spent: float


class BudgetLimitData(BaseData):
    """
    Class representing the data of a budget.

    Attributes:
        attributes (BudgetAttributes): The attributes of the budget.
    """

    attributes: BudgetLimitAttrebutes


class BudgetLimitsModel(BaseFireflyModel):
    """
    Represents a budget limit returned by the API.

    Attributes:
        data (list[BudgetLimitAttrebutes]): A list of BudgetLimitAttributes objects representing the budget limits returned by the API.
    """

    data: list[BudgetLimitData]


class BudgetTransactionData(BaseData):
    attributes: TransactionAttributes


class BudgetTransactionsModel(BaseFireflyModel):
    data: list[BudgetTransactionData]
