from __future__ import annotations
from typing import TYPE_CHECKING

import aiogram
import ujson

from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.utils import formatting
from loguru import logger
from firefly_report_bot.config import TelegramSettings
from firefly_report_bot.bot.routers.root import RootRouter
from firefly_report_bot.bot.routers.accounts import AccountsRouter
from firefly_report_bot.bot.routers.transactions import TransactionsRouter
from firefly_report_bot.bot.routers.report import ReportRouter
from firefly_report_bot.bot.routers.budget import BudgetRouter
from firefly_report_bot.bot.routers.categories import CategoriesRouter

if TYPE_CHECKING:
    from firefly_report_bot.client import FireflyClient


class Bot:
    def __init__(self, settings: TelegramSettings, client: FireflyClient, day_period: int = 5) -> None:
        """
        Initializes the Bot class with the provided settings, client, and optional day_period.

        Parameters:
            settings (TelegramSettings): The settings for the Telegram bot.
            client (FireflyClient): The client for interacting with the Firefly API.
            day_period (int, optional): The period of days. Defaults to 5.

        Returns:
            None
        """

        self.timeout = settings.api_request_timeout
        self.chat_id = settings.chat_id
        self.day_period = day_period
        self.client = client
        session = AiohttpSession(
            proxy=settings.proxy_url, timeout=self.timeout, json_loads=ujson.loads, json_dumps=ujson.dumps
        )
        self.bot = aiogram.Bot(
            token=settings.bot_token, default=DefaultBotProperties(parse_mode="HTML"), session=session
        )
        self.dispatcher = aiogram.Dispatcher(disable_fsm=True)
        self.dispatcher.include_router(TransactionsRouter(client=self.client).get_router())
        self.dispatcher.include_router(AccountsRouter(client=self.client).get_router())
        self.dispatcher.include_router(ReportRouter(client=self.client).get_router())
        self.dispatcher.include_router(BudgetRouter(client=self.client).get_router())
        self.dispatcher.include_router(CategoriesRouter(client=self.client).get_router())
        self.dispatcher.include_router(RootRouter(client=self.client).get_router())
        logger.info("[BOT] Telegram bot started")

    async def send_message(self, message: formatting.Text) -> int:
        """
        Asynchronously sends a message to the chat.

        Args:
            message (formatting.Text): The message to send.

        Returns:
            int: The ID of the sent message.
        """

        tg_message = await self.bot.send_message(chat_id=self.chat_id, text=message.as_html())
        return tg_message.message_id
