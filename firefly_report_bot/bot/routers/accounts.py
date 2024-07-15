from aiogram import Router, F, types
from aiogram.utils import formatting
from loguru import logger
from firefly_report_bot.bot.routers.base import BaseRoter
from firefly_report_bot.bot.keyboards import get_accounts_inline_kb
from firefly_report_bot.client.enums import AccountType


class AccountsRouter(BaseRoter):
    router = Router(name="accounts_router")

    def get_router(self) -> Router:
        self.router.message(F.text == "💳 Accounts")(self.get_accounts)
        self.router.callback_query(F.data.lower() == "account/asset")(self.get_asset_accounts)
        self.router.callback_query(F.data.lower() == "account/revenue")(self.get_revenue_accounts)
        self.router.callback_query(F.data.lower() == "account/expense")(self.get_expense_accounts)
        self.router.callback_query(F.data.lower() == "account/liabilities")(self.get_liabilities_accounts)
        self.router.callback_query(F.data.lower() == "account/ok")(self.accounts_ok)
        return self.router

    async def _get_accounts(self, account_type: AccountType = AccountType.ASSET) -> formatting.Text:
        """
        Retrieves a list of accounts of the specified account type.

        Args:
            account_type (AccountType, optional): The type of account to retrieve. Defaults to AccountType.ASSET.

        Returns:
            formatting.Text: A formatted text containing the list of accounts.

        Raises:
            None

        """

        accounts = await self.client.get_accounts(account_type=account_type)
        sections = [formatting.as_section(formatting.Bold(f"🟢 {account_type.value.capitalize()} accounts: 🟢"))]
        if not accounts:
            sections.append(formatting.as_section("No accounts found."))
            return formatting.as_section(*sections)
        for account in accounts:
            sections.append(
                formatting.as_key_value(account.name, f"{account.current_balance} ({account.currency_code})\n")
            )
        return formatting.as_section(*sections)

    async def get_accounts(self, message: types.Message) -> None:
        """
        Retrieves a list of accounts of the specified account type.

        Args:
            account_type (AccountType, optional): The type of account to retrieve. Defaults to AccountType.ASSET.

        Returns:
            formatting.Text: A formatted text containing the list of accounts.
        """

        logger.info(f"[BOT] Accounts message from user {message.from_user.id if message.from_user else None}")
        text = await self._get_accounts()
        await message.answer(
            text=text.as_html(), reply_markup=get_accounts_inline_kb(current_account_type=AccountType.ASSET)
        )

    async def get_asset_accounts(self, callback: types.CallbackQuery) -> None:
        """
        Retrieves asset accounts and updates the callback message with the formatted account information.

        Args:
            callback (types.CallbackQuery): The callback query triggering this function.

        Returns:
            None
        """

        logger.info(f"[BOT] Asset accounts callback from user {callback.from_user.id}")
        text = await self._get_accounts(account_type=AccountType.ASSET)
        if callback.message is None or isinstance(callback.message, types.InaccessibleMessage):
            await callback.answer("Internal error")
            return
        await callback.message.edit_text(text.as_html())
        await callback.message.edit_reply_markup(
            reply_markup=get_accounts_inline_kb(current_account_type=AccountType.ASSET)
        )
        await callback.answer()

    async def get_revenue_accounts(self, callback: types.CallbackQuery) -> None:
        """
        Retrieves revenue accounts and updates the callback message with the formatted account information.

        Args:
            callback (types.CallbackQuery): The callback query triggering this function.

        Returns:
            None
        """

        logger.info(f"[BOT] Revenue accounts callback from user {callback.from_user.id}")
        text = await self._get_accounts(account_type=AccountType.REVENUE)
        if callback.message is None or isinstance(callback.message, types.InaccessibleMessage):
            await callback.answer("Internal error")
            return
        await callback.message.edit_text(text.as_html())
        await callback.message.edit_reply_markup(
            reply_markup=get_accounts_inline_kb(current_account_type=AccountType.REVENUE)
        )
        await callback.answer()

    async def get_expense_accounts(self, callback: types.CallbackQuery) -> None:
        """
        Retrieves expense accounts and updates the callback message with the formatted account information.

        Args:
            callback (types.CallbackQuery): The callback query triggering this function.

        Returns:
            None
        """
        logger.info(f"[BOT] Expense accounts callback from user {callback.from_user.id}")
        text = await self._get_accounts(account_type=AccountType.EXPENSE)
        if callback.message is None or isinstance(callback.message, types.InaccessibleMessage):
            await callback.answer("Internal error")
            return
        await callback.message.edit_text(text.as_html())
        await callback.message.edit_reply_markup(
            reply_markup=get_accounts_inline_kb(current_account_type=AccountType.EXPENSE)
        )
        await callback.answer()

    async def get_liabilities_accounts(self, callback: types.CallbackQuery) -> None:
        """
        Retrieves liabilities accounts and updates the callback message with the formatted account information.

        Args:
            self: The AccountsRouter instance.
            callback (types.CallbackQuery): The callback query triggering this function.

        Returns:
            None
        """

        logger.info(f"[BOT] Liabilities accounts callback from user {callback.from_user.id}")
        text = await self._get_accounts(account_type=AccountType.LIABILITIES)
        if callback.message is None or isinstance(callback.message, types.InaccessibleMessage):
            await callback.answer("Internal error")
            return
        await callback.message.edit_text(text.as_html())
        await callback.message.edit_reply_markup(
            reply_markup=get_accounts_inline_kb(current_account_type=AccountType.LIABILITIES)
        )
        await callback.answer()

    async def accounts_ok(self, callback: types.CallbackQuery) -> None:
        """
        Deletes the message associated with the callback.

        Args:
            callback (types.CallbackQuery): The callback query triggering this function.

        Returns:
            None
        """

        logger.info(f"[BOT] Accounts OK callback from user {callback.from_user.id}")
        if callback.message is None or isinstance(callback.message, types.InaccessibleMessage):
            return
        await callback.message.delete()
