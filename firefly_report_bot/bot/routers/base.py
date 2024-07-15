from __future__ import annotations
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod
from aiogram import Router

if TYPE_CHECKING:
    from firefly_report_bot.client import FireflyClient


class BaseRoter(ABC):
    router: Router | None = None

    def __new__(cls, *args, **kwargs):
        """
        A special method that creates and returns a new instance of a class.
        It checks if the router attribute of the class is None and raises a NotImplementedError if so.
        Returns the new instance created.
        """

        if cls.router is None:
            raise NotImplementedError("Router is not implemented")
        return object.__new__(cls)

    def __init__(self, client: FireflyClient) -> None:
        """
        Initializes the BaseRoter class with the provided client.

        Args:
            client (FireflyClient): The client for interacting with the Firefly API.

        Returns:
            None
        """

        self.client = client

    @abstractmethod
    def get_router(self) -> Router:
        """
        A description of the entire function, its parameters, and its return types.
        """

        ...
