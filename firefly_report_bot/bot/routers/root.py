from loguru import logger
from aiogram import Router
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command
from firefly_report_bot.bot.keyboards import get_main_kb
from firefly_report_bot.bot.routers.base import BaseRoter


class RootRouter(BaseRoter):
    router = Router(name="root_router")

    def get_router(self) -> Router:
        """
        Initializes the start and stop commands from a user.

        Returns:
            Router: The router object.
        """
        self.router.message(Command("start"))(self.start)
        self.router.message(Command("stop"))(self.stop)
        return self.router

    async def start(self, message: Message):
        """
        Asynchronously handles the start command from a user.

        Args:
            message (Message): The message object containing the user's start command.

        Returns:
            None
        """

        logger.info(f"[BOT] Start command from user {message.from_user.id if message.from_user else None}")
        await message.answer("Hi", reply_markup=get_main_kb())

    async def stop(self, message: Message):
        """
        Asynchronously handles the stop command from a user.

        Args:
            message (Message): The message object containing the user's stop command.

        Returns:
            None
        """

        logger.info(f"[BOT] Bye command from user {message.from_user.id if message.from_user else None}")
        await message.answer("Bye", reply_markup=ReplyKeyboardRemove())
