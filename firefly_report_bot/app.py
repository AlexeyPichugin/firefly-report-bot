from firefly_report_bot.client import FireflyClient
from firefly_report_bot.bot import Bot
from firefly_report_bot.config import get_settings
from firefly_report_bot.reports import get_reports
from loguru import logger
import sys
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler


class App:
    def __init__(self):
        """
        Initializes the App class with the provided settings, client, and optional day_period.

        This method tries to load the settings file using the `get_settings` function. If the file is not found,
        it logs an error message and exits the program. If any other exception occurs while loading the settings,
        it logs an error message with the exception details and exits the program.

        After loading the settings, it removes the default logger and adds a new logger that logs messages to
        the standard error stream with the log level specified in the settings. It then logs an info message
        indicating that the settings file has been loaded.

        Finally, it initializes the `client` attribute with a `FireflyClient` instance using the settings from the
        loaded settings file. It initializes the `bot` attribute with a `Bot` instance using the settings from the
        loaded settings file and the `client` attribute.

        Parameters:
            None

        Returns:
            None
        """
        try:

            self.settings = get_settings()
        except FileNotFoundError:
            logger.error("[APP] Settings file not found")
            sys.exit()
        except Exception as e:
            logger.error(f"[APP] Settings file error: {e}")
            sys.exit()
        logger.remove()
        logger.add(sys.stderr, level=self.settings.log_level.value.upper())
        logger.info("[APP] Settings file loaded")
        self.client = FireflyClient(settings=self.settings.firefly)
        self.bot = Bot(settings=self.settings.telegram, client=self.client, day_period=self.settings.day_period)

    async def send_report_message(self):
        """
        Asynchronously sends report messages for each report in the reports list.

        Parameters:
            None

        Returns:
            None
        """
        reports = get_reports()
        for report in reports:
            message = await report.generate(self.client)
            await self.bot.send_message(message=message)
            logger.info(f"[APP] Message sent: {report.header}")
            await asyncio.sleep(self.settings.telegram.api_request_timeout)

    async def get_transactions(self):
        """
        Asynchronously gets transactions using the client object.
        """
        await self.client.get_transactions()

    async def start_shcheduler(self):
        """
        Asynchronously starts a scheduler to send report messages at the specified time.

        This function creates an instance of the `AsyncIOScheduler` class and adds a job to it using the `add_job` method.
        The job is set to run at the specified time specified by the `send_report_message` method.

        Parameters:
            None

        Returns:
            None
        """
        scheduler = AsyncIOScheduler()
        scheduler.add_job(
            self.send_report_message,
            "cron",
            year="*",
            month="*",
            day="*",
            hour=str(self.settings.send_report_hour),
            minute=str(self.settings.send_report_minute),
            second="0",
        )
        scheduler.start()

    async def run(self):
        """
        Asynchronously runs the application.

        This function logs that the app has started, creates a task to start the scheduler,
        and then starts polling the bot dispatcher.

        Parameters:
            None

        Returns:
            None
        """
        logger.info("[APP] App started")
        asyncio.create_task(self.start_shcheduler())
        await self.bot.dispatcher.start_polling(self.bot.bot, polling_timeout=self.bot.timeout)
