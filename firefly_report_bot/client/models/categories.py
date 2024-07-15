from datetime import datetime
from pydantic import BaseModel, Field
from firefly_report_bot.client.models.base import BaseAttributes, BaseFireflyModel, BaseData


class CategorySpent(BaseModel):
    """
    Represents a category of spent transactions.

    Attributes:
        sum (float or None): The total amount spent in this category.
        currency_id (str or None): The ID of the currency.
        currency_code (str or None): The code of the currency.
        currency_symbol (str or None): The symbol of the currency.
        currency_decimal_places (int or None): The number of decimal places for the currency.
    """

    sum: float | None = None
    currency_id: int | None = None
    currency_code: str | None = None
    currency_symbol: str | None = None
    currency_decimal_places: int | None = None


class CategoryEarned(BaseModel):
    """
    Represents a category of earned transactions.

    Attributes:
        sum (float or None): The total amount earned in this category.
        currency_id (str or None): The ID of the currency.
        currency_code (str or None): The code of the currency.
        currency_symbol (str or None): The symbol of the currency.
        currency_decimal_places (int or None): The number of decimal places for the currency.
    """

    sum: float | None = None
    currency_id: int | None = None
    currency_code: str | None = None
    currency_symbol: str | None = None
    currency_decimal_places: int | None = None


class CategoryAttributes(BaseAttributes):
    """
    Represents the attributes of a category.

    Attributes:
        created_at (datetime or None): The datetime when the category was created.
        updated_at (datetime or None): The datetime when the category was last updated.
        name (str): The name of the category.
        notes (str or None): Additional notes for the category.
        spent (list[CategorySpent]): The list of amounts spent in the category.
        earned (list[CategoryEarned]): The list of amounts earned in the category.
    """

    created_at: datetime | None = None
    updated_at: datetime | None = None
    name: str
    notes: str | None = None
    spent: list[CategorySpent] = Field(..., default_factory=list)
    earned: list[CategoryEarned] = Field(..., default_factory=list)


class CategoryData(BaseData):
    """
    Represents the data of a category.

    Attributes:
        attributes (CategoryAttributes): The attributes of the category.
    """

    attributes: CategoryAttributes


class CategoriesModel(BaseFireflyModel):
    """
    Represents a list of categories.

    Attributes:
        data (list[CategoryData]): The list of categories.
    """

    data: list[CategoryData]


class CategoryModel(BaseFireflyModel):
    """
    Represents a category.

    Attributes:
        data (CategoryData): The data of the category.
    """

    data: CategoryData
