from datetime import datetime
from pydantic import Field
from firefly_report_bot.client.models.base import BaseAttributes, BaseFireflyModel, BaseData
from firefly_report_bot.client.enums import (
    FireflyAccountType,
    AccountRole,
    CreditCardType,
    LiabilityType,
    LiabilityDirection,
    InterestPeriod,
)


class AccountAttributes(BaseAttributes):
    """
    Class representing attributes of an account.

    Attributes:
        created_at (datetime): The datetime when the account was created.
        updated_at (datetime): The datetime when the account was last updated.
        active (bool): Flag indicating if the account is active.
        order (int): The order of the account.
        name (str): The name of the account.
        type (FireflyAccountType): The type of the account.
        account_role (AccountRole): The role of the account.
        currency_id (str): The ID of the currency.
        currency_code (str): The code of the currency.
        currency_symbol (str): The symbol of the currency.
        currency_decimal_places (int): The number of decimal places for the currency.
        current_balance (float): The current balance of the account.
        current_balance_date (datetime): The date of the current balance.
        iban (str): The IBAN of the account.
        bic (str): The BIC of the account.
        account_number (str): The account number.
        opening_balance (float): The opening balance of the account.
        current_debt (float): The current debt of the account.
        opening_balance_date (datetime): The date of the opening balance.
        virtual_balance (float): The virtual balance of the account.
        include_net_worth (bool): Flag indicating if net worth is included.
        credit_card_type (CreditCardType): The type of credit card.
        monthly_payment_date (datetime): The date of the monthly payment.
        liability_type (LiabilityType): The type of liability.
        liability_direction (LiabilityDirection): The direction of the liability.
        interest (float): The interest rate.
        interest_period (InterestPeriod): The period of interest.
        notes (str): Additional notes.
        latitude (float): The latitude of the account.
        longitude (float): The longitude of the account.
        zoom_level (int): The zoom level of the account.
    """

    created_at: datetime | None = None
    updated_at: datetime | None = None
    active: bool = True
    order: int | None = None
    name: str
    type: FireflyAccountType | None = Field(None)
    account_role: AccountRole | None = Field(None)
    currency_id: int | None = None
    currency_code: str | None = None
    currency_symbol: str | None = None
    currency_decimal_places: int | None = None
    current_balance: float | None = None
    current_balance_date: datetime | None = None
    iban: str | None = None
    bic: str | None = None
    account_number: str | None = None
    opening_balance: float | None = None
    current_debt: float | None = None
    opening_balance_date: datetime | None = None
    virtual_balance: float | None = None
    include_net_worth: bool = True
    credit_card_type: CreditCardType | None = Field(None)
    monthly_payment_date: datetime | None = None
    liability_type: LiabilityType | None = Field(None)
    liability_direction: LiabilityDirection | None = Field(None)
    interest: float | None = None
    interest_period: InterestPeriod | None = Field(None)
    notes: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    zoom_level: int | None = None


class AccountData(BaseData):
    """
    Class representing an account data.

    Attributes:
        attributes (AccountAttributes): The attributes of the account.
    """

    attributes: AccountAttributes


class AccountsModel(BaseFireflyModel):
    """
    Class representing a collection of account data.

    Attributes:
        data (list[AccountData]): A list of account data.
    """

    data: list[AccountData]


"""
Class representing an account.

Attributes:
    data (AccountData): The data of the account.
"""


class AccountModel(BaseFireflyModel):
    data: AccountData
