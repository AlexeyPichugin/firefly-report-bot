from aiogram import Router, F, types
from aiogram.utils import formatting
from loguru import logger
from datetime import datetime
from firefly_report_bot.bot.routers.base import BaseRoter
from firefly_report_bot.bot.keyboards import get_budgets_inline_kb
from firefly_report_bot.client.classes import Transaction


class BudgetRouter(BaseRoter):
    router = Router(name="budget_router")

    def get_router(self) -> Router:
        """
        Get the router for handling budget requests.

        This method initializes the router with a message handler that triggers the `get_budget` method when the user sends a message with the text "📊 Budgets".

        Returns:
            Router: The router object.
        """

        self.router.message(F.text == "📊 Budgets")(self.get_budget)
        self.router.callback_query(F.data.lower() == "budgets/ok")(self.budgets_ok)
        self.router.callback_query(F.data.lower().startswith("budget/"))(self.get_budget_transactions)
        return self.router

    async def get_budget(self, message: types.Message) -> None:
        """
        Retrieves the budget information for the user and sends a formatted message with the budget details.

        Args:
            message (types.Message): The message object containing information about the user.

        Returns:
            None
        """

        logger.info(f"[BOT] Budget request from user {message.from_user.id if message.from_user else None}")
        start_dttm = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        end_dttm = datetime.now().replace(month=12, day=31, hour=23, minute=59, second=59, microsecond=0)
        budgets = await self.client.get_budgets(start_dttm=start_dttm, end_dttm=end_dttm)
        sections = [formatting.Bold("📊 Budgets"), formatting.Text("\n")]
        for budget in budgets:
            transactions = await self.client.get_transactions(start_dttm=start_dttm, end_dttm=end_dttm)
            spent = sum(
                transaction.amount or 0 for transaction in transactions if transaction.budget_name == budget.name
            )
            value = f"{spent:.2f} / {budget.limit if budget.limit else 0}"
            if budget.limit:
                used = int((spent / budget.limit) * 100)
                value += f" ({used}%)"
                symbol = "✅" if spent <= budget.limit else "❌"
            else:
                symbol = "✅" if spent == 0 else "❌"
            sections.append(formatting.as_key_value(f"{symbol} {budget.name}", value + "\n"))
        await message.answer(
            formatting.as_section(*sections).as_html(),
            reply_markup=get_budgets_inline_kb(budgets=[budget.name for budget in budgets]),
        )

    async def budgets_ok(self, callback: types.CallbackQuery) -> None:
        """
        Asynchronously handles the budgets_ok callback from the user.

        Deletes the message associated with the callback.

        Args:
            callback (types.CallbackQuery): The callback query triggering this function.

        Returns:
            None
        """
        logger.info(f"[BOT] Budgets OK callback from user {callback.from_user.id}")
        if callback.message is None or isinstance(callback.message, types.InaccessibleMessage):
            return
        await callback.message.delete()

    def _format_transactions(self, transactions: list[Transaction]) -> list[formatting.Text]:
        """
        Formats a list of Transaction objects into a list of formatted sections.

        Args:
            transactions (list[Transaction]): The transactions to format.

        Returns:
            list[formatting.Text]: The formatted sections.
        """
        sections = [formatting.Text(formatting.Bold("🟢 Transactions"))]
        if not transactions:
            sections.append(formatting.as_section("No transactions found.\n"))
            return sections
        for transaction in transactions:
            sections.append(
                formatting.as_key_value(
                    f"- {transaction.created_at:%Y-%m-%d} [{transaction.source_name}] {transaction.budget_name}",
                    f"{transaction.amount} ({transaction.description})\n",
                )
            )
        return sections

    async def get_budget_transactions(self, callback: types.CallbackQuery) -> None:
        """
        Asynchronously handles the get_budget_transactions callback from the user.

        Retrieves transactions for the specified budget and updates the callback message with the formatted transaction information.

        Args:
            callback (types.CallbackQuery): The callback query object triggering the transaction retrieval.

        Returns:
            None
        """
        logger.info(f"[BOT] Budget transactions callback from user {callback.from_user.id}")
        if callback.data is None:
            await callback.answer("Internal error")
            return
        budget_name = callback.data.split("/")[-1]
        start_dttm = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        end_dttm = datetime.now().replace(hour=23, minute=59, second=59, microsecond=0)
        _transactions = await self.client.get_transactions(start_dttm=start_dttm, end_dttm=end_dttm)
        transactions = [transaction for transaction in _transactions if transaction.budget_name == budget_name]
        if transactions:
            transactions.sort(key=lambda transaction: transaction.created_at, reverse=True)  # type: ignore
        text = formatting.as_section(*self._format_transactions(transactions))
        if callback.message is None or isinstance(callback.message, types.InaccessibleMessage):
            await callback.answer("Internal error")
            return
        await callback.message.edit_text(text=text.as_html())
        await callback.message.edit_reply_markup(reply_markup=get_budgets_inline_kb(budgets=[]))
        await callback.answer()
