from loguru import logger
from aiogram import Router, F, types
from datetime import datetime, timedelta
from firefly_report_bot.bot.keyboards import get_reports_inline_kb
from firefly_report_bot.bot.routers.base import BaseRoter
from firefly_report_bot.config import get_settings
from firefly_report_bot.reports import DaylyReport, MonthlyReport, LastNDaysReport


class ReportRouter(BaseRoter):
    router = Router(name="report_router")

    def get_router(self) -> Router:
        """
        A method that configures message and callback query handlers for various report types.
        This function returns the configured router for handling reports.
        """
        self.router.message(F.text == "📈 Reports")(self.get_report)
        self.router.callback_query(F.data == "report/daily")(self.daily_report)
        self.router.callback_query(F.data == "report/monthly")(self.monthly_report)
        self.router.callback_query(F.data == "report/periodic")(self.periodic_reports)
        return self.router

    async def get_report(self, message: types.Message):
        """
        Asynchronously handles the "get report" message from a user.

        Args:
            message (types.Message): The message object containing the user's request.

        Returns:
            None
        """
        logger.info(f"[BOT] Start get repors message from user {message.from_user.id if message.from_user else None}")
        await message.answer("Choose type of report", reply_markup=get_reports_inline_kb())

    async def daily_report(self, callback: types.CallbackQuery):
        """
        Asynchronously handles the daily report request from a user.

        Args:
            callback (types.CallbackQuery): The callback query object triggering the report.

        Returns:
            None
        """
        logger.info(f"[BOT] Daily report request from user {callback.from_user.id}")
        yesterday = datetime.now() - timedelta(days=1)
        report = DaylyReport(
            header=f"Daily report: {yesterday.strftime('%Y-%m-%d')}",
            start_dttm=yesterday.replace(hour=0, minute=0, second=0),
            end_dttm=yesterday.replace(hour=23, minute=59, second=59),
        )
        text = await report.generate(self.client)
        if callback.message is None or isinstance(callback.message, types.InaccessibleMessage):
            await callback.answer("Internal error")
            return
        await callback.message.answer(text=text.as_html())
        await callback.message.delete()
        await callback.answer()

    async def monthly_report(self, callback: types.CallbackQuery):
        """
        Asynchronously handles the monthly report request from a user.

        Args:
            callback (types.CallbackQuery): The callback query object triggering the report.

        Returns:
            None
        """
        logger.info(f"[BOT] Monthly report request from user {callback.from_user.id}")
        yesterday = datetime.now() - timedelta(days=1)
        report = MonthlyReport(
            header=f"Monthly report: {yesterday.strftime('%Y-%m')}",
            start_dttm=yesterday.replace(day=1, hour=0, minute=0, second=0),
            end_dttm=yesterday.replace(hour=23, minute=59, second=59),
        )
        text = await report.generate(self.client)
        if callback.message is None or isinstance(callback.message, types.InaccessibleMessage):
            await callback.answer("Internal error")
            return
        await callback.message.answer(text=text.as_html())
        await callback.message.delete()
        await callback.answer()

    async def periodic_reports(self, callback: types.CallbackQuery):
        """
        Asynchronously handles the periodic reports request from a user.

        Args:
            self: The current object instance.
            callback (types.CallbackQuery): The callback query object triggering the report.

        Returns:
            None
        """
        settings = get_settings()
        logger.info(f"[BOT] Periodic report request from user {callback.from_user.id}")
        yesterday = datetime.now() - timedelta(days=1)
        start_dttm = (yesterday - timedelta(days=settings.day_period)).replace(hour=0, minute=0, second=0)
        end_dttm = yesterday.replace(hour=23, minute=59, second=59)
        report = LastNDaysReport(
            header=f"Last {settings.day_period} days report: {start_dttm.strftime('%Y-%m')} {start_dttm.day}-{end_dttm.day}",
            start_dttm=start_dttm,
            end_dttm=end_dttm,
        )
        text = await report.generate(self.client)
        if callback.message is None or isinstance(callback.message, types.InaccessibleMessage):
            await callback.answer("Internal error")
            return
        await callback.message.answer(text=text.as_html())
        await callback.message.delete()
        await callback.answer()
