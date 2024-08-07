from aiogram import Router, F, types
from aiogram.utils import formatting
from loguru import logger
from datetime import datetime
from firefly_report_bot.bot.routers.base import BaseRoter


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
        await message.answer(formatting.as_section(*sections).as_html())
