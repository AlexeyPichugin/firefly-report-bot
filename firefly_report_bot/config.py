from __future__ import annotations
from typing import Type
from pydantic_settings import BaseSettings, YamlConfigSettingsSource, PydanticBaseSettingsSource
from pydantic import BaseModel, Field
from functools import lru_cache
from enum import Enum


class LogLevel(str, Enum):
    """
    Enum representing different log levels.

    Attributes:
        DEBUG (str): Debug level log messages.
        INFO (str): Informational level log messages.
        WARNING (str): Warning level log messages.
        ERROR (str): Error level log messages.
        CRITICAL (str): Critical level log messages.
    """

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class FireflyClientSettings(BaseModel):
    """
    Represents the settings for the Firefly client.

    Attributes:
        api_key (str): The API key for the Firefly client.
        api_url (str): The API URL for the Firefly client.
        request_timeout (int, optional): The request timeout for the Firefly client. Defaults to 60.
    """

    api_key: str
    api_url: str
    request_timeout: int = 60


class TelegramSettings(BaseModel):
    """
    Represents the settings for the Telegram bot.

    Attributes:
        bot_token (str): The token for the Telegram bot.
        chat_id (int): The chat ID for the Telegram bot.
        proxy_url (str, optional): The proxy URL for the Telegram bot. Defaults to None.
        api_request_timeout (int): The API request timeout for the Telegram bot. Default is 60.
    """

    bot_token: str
    chat_id: int
    proxy_url: str | None = None
    api_request_timeout: int = 60


class ReportSettings(BaseModel):
    """
    Represents the settings for the report generation.

    Attributes:
        send_report (bool): Flag indicating whether to send the report.
        exclude_budgets (list[str]): The list of budget names to exclude from the report.
        exclude_categories (list[str]): The list of category names to exclude from the report.
    """

    send_report: bool = True
    exclude_budgets: list[str] = Field(..., default_factory=list)
    exclude_categories: list[str] = Field(..., default_factory=list)


class Settings(BaseSettings):
    """
    Represents the settings for the application.

    Attributes:
        firefly (FireflyClientSettings): The settings for the Firefly client.
        telegram (TelegramSettings): The settings for the Telegram bot.
        log_level (LogLevel): The log level for the application. Defaults to "INFO".
        day_period (int): The period in days for generating reports. Defaults to 5.
        send_report_hour (int): The hour at which to send reports. Defaults to 12.
        send_report_minute (int): The minute at which to send reports. Defaults to 0.
        daily_report (ReportSettings): The settings for generating daily reports.
        monthly_report (ReportSettings): The settings for generating monthly reports.
        periodic_report (ReportSettings): The settings for generating periodic reports.
    """

    firefly: FireflyClientSettings
    telegram: TelegramSettings
    log_level: LogLevel = LogLevel.INFO
    categories_in_row: int = 2
    day_period: int = 5
    send_report_hour: int = 12
    send_report_minute: int = 0
    daily_report: ReportSettings = ReportSettings()
    monthly_report: ReportSettings = ReportSettings()
    periodic_report: ReportSettings = ReportSettings()

    @classmethod
    def settings_customise_sources(  # type: ignore
        cls, settings_cls: Type[BaseSettings], **kwargs
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        """
        Customizes the settings sources for the given settings class.

        Args:
            settings_cls (Type[BaseSettings]): The settings class to customize.
            **kwargs: Additional keyword arguments.

        Returns:
            tuple[PydanticBaseSettingsSource, ...]: A tuple of PydanticBaseSettingsSource objects representing the customized settings sources.

        """
        return (
            YamlConfigSettingsSource(
                settings_cls=settings_cls,
                yaml_file="./settings.yaml",
                yaml_file_encoding="utf-8",
            ),
        )


@lru_cache
def get_settings() -> Settings:
    """
    Retrieves the settings using caching mechanism.

    Returns:
        Settings: The settings object.
    """
    return Settings()  # type: ignore
