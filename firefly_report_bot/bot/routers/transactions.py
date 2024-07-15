from aiogram import Router, F, types
from aiogram.utils import formatting
from loguru import logger
from datetime import datetime
from firefly_report_bot.bot.routers.base import BaseRoter
from firefly_report_bot.bot.keyboards import get_transactions_inline_kb
from firefly_report_bot.client.enums import TransactionType


class TransactionsRouter(BaseRoter):
    router = Router(name="accounts_router")

    def get_router(self) -> Router:
        """
        A method that defines the router for handling transactions.
        It sets up message and callback query handlers for different transaction scenarios.
        Returns the configured router for transactions.
        """

        self.router.message(F.text == "🔀 Transactions")(self.get_transactions)
        self.router.callback_query(F.data.lower() == "transactions/ok")(self.transactions_ok)
        self.router.callback_query(F.data.startswith("transactions/"))(self.get_minus_for_date)
        return self.router

    async def _get_transactions(self, dttm: datetime) -> formatting.Text:
        """
        Retrieves transactions for a given date and formats them into sections.

        Args:
            dttm (datetime): The date for which to retrieve transactions.

        Returns:
            formatting.Text: The formatted sections containing the transactions.
        """

        sections = [formatting.as_section(formatting.Bold(f"🟢 Transactions {dttm.strftime("%Y-%m-%d")}"))]
        for transaction_type in [TransactionType.WITHDRAWAL, TransactionType.DEPOSIT, TransactionType.TRANSFER]:
            transactions = await self.client.get_transactions(
                transaction_type=transaction_type, start_dttm=dttm, end_dttm=dttm
            )
            sections.append(formatting.as_section(formatting.Bold(f"🟢 {transaction_type.value.capitalize()}")))
            if not transactions:
                sections.append(formatting.as_section("No transactions found.\n"))
                continue
            for transaction in transactions:
                sections.append(
                    formatting.as_key_value(
                        f"[{transaction.source_name}] {transaction.category_name} {transaction.budget_name}",
                        f"{transaction.amount} ({transaction.description})\n",
                    )
                )
            sections.append(formatting.as_section("\n"))
        return formatting.as_section(*sections)

    async def get_transactions(self, message: types.Message):
        """
        Asynchronously handles the get_transactions message from a user.

        Args:
            message (types.Message): The message object containing the user's get_transactions command.

        Returns:
            None
        """
        logger.info(f"[BOT] Transactions message from user {message.from_user.id if message.from_user else None}")
        text = await self._get_transactions(dttm=datetime.now())
        await message.reply(text=text.as_html(), reply_markup=get_transactions_inline_kb())

    async def get_minus_for_date(self, callback: types.CallbackQuery):
        """
        Asynchronously handles the get_minus_for_date callback from the user.

        Args:
            self: The TransactionsRouter object.
            callback (types.CallbackQuery): The callback query object.

        Returns:
            None
        """

        if callback.message is None or isinstance(callback.message, types.InaccessibleMessage):
            await callback.answer("Internal error")
            return
        logger.info(f"[BOT] Transactions minus day callback from user {callback.from_user.id}")
        if callback.data is None:
            await callback.answer("Internal error")
            return
        str_dttm = callback.data.removeprefix("transactions/")
        dttm = datetime.strptime(str_dttm, "%Y-%m-%d")
        text = await self._get_transactions(dttm=dttm)
        await callback.message.edit_text(text.as_html())
        await callback.message.edit_reply_markup(reply_markup=get_transactions_inline_kb(dttm=dttm))
        await callback.answer()

    async def transactions_ok(self, callback: types.CallbackQuery):
        """
        Asynchronously handles the transactions_ok callback from the user.

        Args:
            self: The TransactionsRouter object.
            callback (types.CallbackQuery): The callback query object.

        Returns:
            None
        """

        logger.info(f"[BOT] Accounts OK callback from user {callback.from_user.id}")
        if callback.message is None or isinstance(callback.message, types.InaccessibleMessage):
            return
        await callback.message.delete()
