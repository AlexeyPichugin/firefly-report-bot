from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram import types
from datetime import datetime, timedelta

from firefly_report_bot.client.enums import AccountType
from firefly_report_bot.config import get_settings


def get_main_kb() -> types.ReplyKeyboardMarkup:
    """
    Generates an inline keyboard for transaction options based on the provided date.

    Args:
        dttm (datetime | None): The date and time for which to generate the keyboard. Defaults to None.

    Returns:
        types.InlineKeyboardMarkup: The inline keyboard markup for the transaction options.
    """

    buidler = ReplyKeyboardBuilder()
    buidler.add(
        types.KeyboardButton(text="💳 Accounts"),
        types.KeyboardButton(text="🔀 Transactions"),
        types.KeyboardButton(text="📊 Budgets"),
        types.KeyboardButton(text="📈 Reports"),
    )
    buidler.adjust(2)
    return buidler.as_markup(resize_keyboard=True)


def get_accounts_inline_kb(current_account_type: AccountType = AccountType.ASSET) -> types.InlineKeyboardMarkup:
    """
    Generates an inline keyboard for account options based on the provided current account type.

    Args:
        current_account_type (AccountType): The current account type. Defaults to ASSET.

    Returns:
        types.InlineKeyboardMarkup: The inline keyboard markup for the account options.
    """

    builder = InlineKeyboardBuilder()
    accounts_types: set[AccountType] = {
        AccountType.ASSET,
        AccountType.REVENUE,
        AccountType.EXPENSE,
        AccountType.LIABILITIES,
    }
    accounts_types.remove(current_account_type)
    for account_type in accounts_types:
        builder.row(
            types.InlineKeyboardButton(
                text=account_type.value.capitalize(), callback_data=f"account/{account_type.name}"
            )
        )
    builder.row(types.InlineKeyboardButton(text="✅ OK", callback_data="account/OK"))
    return builder.as_markup()


def get_transactions_inline_kb(dttm: datetime | None = None) -> types.InlineKeyboardMarkup:
    """
    Generates an inline keyboard markup for transaction options based on the given datetime.

    Args:
        dttm (datetime | None): The datetime for which to generate the keyboard. Defaults to None.

    Returns:
        types.InlineKeyboardMarkup: The inline keyboard markup for the transaction options.
    """

    builder = InlineKeyboardBuilder()
    if dttm is None:
        dttm = datetime.now()
    dttm_minus_day = dttm - timedelta(days=1)
    dttm_plus_day = dttm + timedelta(days=1)
    builder.row(
        types.InlineKeyboardButton(
            text=f"<< {dttm_minus_day.strftime('%Y-%m-%d')}",
            callback_data=f"transactions/{dttm_minus_day.strftime('%Y-%m-%d')}",
        ),
        types.InlineKeyboardButton(
            text=f">> {dttm_plus_day.strftime('%Y-%m-%d')}",
            callback_data=f"transactions/{dttm_plus_day.strftime('%Y-%m-%d')}",
        ),
    )
    builder.row(types.InlineKeyboardButton(text="✅ OK", callback_data="transactions/OK"))
    return builder.as_markup()


def get_reports_inline_kb() -> types.InlineKeyboardMarkup:
    """
    Generates an inline keyboard markup for different types of reports.

    Returns:
        types.InlineKeyboardMarkup: The inline keyboard markup for the report options.
    """
    settings = get_settings()

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="📊 Daily report", callback_data="report/daily"))
    builder.row(
        types.InlineKeyboardButton(text=f"📊 {settings.day_period} days report", callback_data="report/periodic")
    )
    builder.row(types.InlineKeyboardButton(text="📊 Monthly report", callback_data="report/monthly"))

    return builder.as_markup()
