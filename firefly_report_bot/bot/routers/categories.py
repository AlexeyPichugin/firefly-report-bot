from aiogram import Router, F, types
from aiogram.utils import formatting
from loguru import logger
from datetime import datetime
from firefly_report_bot.bot.routers.base import BaseRoter
from firefly_report_bot.bot.keyboards import get_categories_inline_kb
from firefly_report_bot.client.classes import Transaction


class CategoriesRouter(BaseRoter):
    router = Router(name="categories_router")

    def get_router(self) -> Router:
        self.router.message(F.text == "🧾 Categories")(self.get_categories)
        self.router.callback_query(F.data.lower() == "categories/ok")(self.categories_ok)
        self.router.callback_query(F.data.lower().startswith("category/"))(self.get_category_transactions)
        return self.router

    async def get_categories(self, message: types.Message) -> None:
        logger.info(f"[BOT] Categories message from user {message.from_user.id if message.from_user else None}")
        categories = await self.client.get_categories()
        text = formatting.Text("Categories")
        await message.reply(
            text=text.as_html(),
            reply_markup=get_categories_inline_kb(categories=[category.name for category in categories]),
        )

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

    async def get_category_transactions(self, callback: types.CallbackQuery) -> None:
        """
        Asynchronously handles the get_category_transactions callback from the user.

        Retrieves transactions for the specified category and updates the callback message with the formatted transaction information.

        Args:
            callback (types.CallbackQuery): The callback query object triggering the transaction retrieval.

        Returns:
            None
        """
        logger.info(f"[BOT] Get category transactions callback from user {callback.from_user.id}")
        if callback.data is None:
            await callback.answer("Internal error")
            return
        category_name = callback.data.split("/")[-1]
        start_dttm = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        end_dttm = datetime.now().replace(hour=23, minute=59, second=59, microsecond=0)
        _transactions = await self.client.get_transactions(start_dttm=start_dttm, end_dttm=end_dttm)
        transactions = [transaction for transaction in _transactions if transaction.category_name == category_name]
        if transactions:
            transactions.sort(key=lambda transaction: transaction.created_at, reverse=True)  # type: ignore
        text = formatting.as_section(*self._format_transactions(transactions))
        if callback.message is None or isinstance(callback.message, types.InaccessibleMessage):
            await callback.answer("Internal error")
            return
        await callback.message.edit_text(text=text.as_html())
        await callback.message.edit_reply_markup(reply_markup=get_categories_inline_kb(categories=[]))
        await callback.answer()

    async def categories_ok(self, callback: types.CallbackQuery) -> None:
        """
        Asynchronously handles the categories_ok callback from the user.

        Deletes the message associated with the callback.

        Args:
            callback (types.CallbackQuery): The callback query triggering this function.

        Returns:
            None
        """
        logger.info(f"[BOT] Categories OK callback from user {callback.from_user.id}")
        if callback.message is None or isinstance(callback.message, types.InaccessibleMessage):
            return
        await callback.message.delete()
