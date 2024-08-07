from __future__ import annotations
from typing import DefaultDict, Sequence
from abc import ABC, abstractmethod
from aiogram.utils import formatting
from datetime import datetime, timedelta
from collections import defaultdict

from firefly_report_bot.client.enums import TransactionType
from firefly_report_bot.client import FireflyClient
from firefly_report_bot.config import get_settings
from calendar import monthrange


class BaseReport(ABC):
    def __init__(self, header: str, start_dttm: datetime, end_dttm: datetime) -> None:
        """
        Initializes the BaseReport object with the provided header, start date time, and end date time.

        Parameters:
            header (str): The header for the report.
            start_dttm (datetime): The start date and time for the report.
            end_dttm (datetime): The end date and time for the report.

        Returns:
            None
        """
        self.header = header
        self.start_dttm = start_dttm
        self.end_dttm = end_dttm

    def get_first_mouth_dttm(self) -> datetime:
        """
        Returns the first day of the month that the report starts at as a datetime object.

        Returns:
            datetime: The first day of the month that the report starts at.
        """
        return self.start_dttm.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    @abstractmethod
    async def generate(self, client: FireflyClient) -> formatting.Text:
        """
        Asynchronously generates a report using the provided client.

        Args:
            client (FireflyClient): The client used to generate the report.

        Returns:
            formatting.Text: The generated report.

        Raises:
            NotImplementedError: This method is an abstract method and must be implemented by subclasses.
        """
        ...

    async def get_summary(
        self, client: FireflyClient, add_months_data: bool = False, add_division: bool = False
    ) -> list[formatting.Text]:
        """
        Asynchronously generates a summary report based on the provided client and additional data options.

        Args:
            self: The current object instance.
            client (FireflyClient): The client used to retrieve transactions.
            add_months_data (bool): Flag to indicate whether to include monthly data in the summary.
            add_division (bool): Flag to indicate whether to include divisional data in the summary.

        Returns:
            list[formatting.Text]: A list of formatted sections containing the summary report.

        Raises:
            None
        """
        sections = []
        for transaction_type in [TransactionType.WITHDRAWAL, TransactionType.DEPOSIT]:
            section_value = ""
            transactions = await client.get_transactions(
                start_dttm=self.start_dttm, end_dttm=self.end_dttm, transaction_type=transaction_type
            )
            transaction_sum = 0
            if transactions:
                transaction_sum = sum([transaction.amount for transaction in transactions])  # type: ignore
            section_value += f"{transaction_sum:.2f}"
            division_sections = []
            if add_division:
                accounts_division: DefaultDict[str, float] = defaultdict(float)
                for transaction in transactions:
                    accounts_division[transaction.source_name or "None"] += transaction.amount or 0

                division_sections = [
                    formatting.as_list(f"{account}: {amount:.2f}\n") for account, amount in accounts_division.items()
                ]
            if add_months_data:
                transactions_month = await client.get_transactions(
                    start_dttm=self.start_dttm, end_dttm=self.end_dttm, transaction_type=transaction_type
                )
                transactions_month_sum = 0
                if transactions_month:
                    transactions_month_sum = sum([transaction.amount for transaction in transactions_month])  # type: ignore
                section_value += f" ({transactions_month_sum:.2f})"
            sections.append(formatting.as_key_value(transaction_type.value.capitalize(), section_value + "\n"))
            for section in division_sections:
                sections.append(section)
        return sections

    async def get_budgets(
        self,
        client: FireflyClient,
        exclude: list[str] | None = None,
        add_periodic_spent: bool = False,
        accumulate_limit: bool = False,
    ) -> list[formatting.Text]:
        """
        Asynchronously retrieves budgets based on certain criteria and formatting options.

        Args:
            self: The current object instance.
            client (FireflyClient): An instance of FireflyClient used to retrieve budgets.
            exclude (list[str] | None, optional): List of budget names to exclude. Defaults to None.
            add_periodic_spent (bool, optional): Flag indicating whether to add periodic spent data. Defaults to False.
            accumulate_limit (bool, optional): Flag indicating whether to accumulate the budget limit. Defaults to False

        Returns:
            list[formatting.Text]: A list of formatted budget sections.
        """
        sections = []
        if exclude is None:
            exclude = []
        budgets = await client.get_budgets(start_dttm=self.get_first_mouth_dttm(), end_dttm=self.end_dttm)
        sections.append(formatting.as_section(formatting.Bold("🟢 Budgets: 🟢\n")))
        for budget in budgets:
            if budget.name in exclude:
                continue
            if add_periodic_spent:
                spent = await self._get_transactions_sum_by_budget(
                    client=client, budget_name=budget.name, start_dttm=self.start_dttm, end_dttm=self.end_dttm
                )
                day_of_month = monthrange(self.start_dttm.year, self.start_dttm.month)[1]

                if accumulate_limit:
                    days_until_end = day_of_month - self.end_dttm.day + 1
                    period_budget = (budget.limit - budget.spent) / days_until_end if budget.limit else 0
                    budget_data = f"{spent:.2f} / {(period_budget if period_budget > 0 else 0):.2f}"
                else:
                    days = (self.end_dttm - self.start_dttm).days + 1
                    period_budget = budget.limit * days / day_of_month
                    budget_data = f"{spent:.2f} / {(period_budget if period_budget > 0 else 0):.2f}"

                if budget.limit:
                    symbol = "✅" if spent <= period_budget else "❌"
                else:
                    symbol = "✅" if spent == 0 else "❌"

                all_spent = budget.spent if budget.spent else 0
                budget_balanse = budget.limit - all_spent
                if budget_balanse > 0:
                    spended_percent = int((budget_balanse / budget.limit) * 100) if budget.limit else 0
                    availible_budget_data = f"Available {budget_balanse:.2f}"
                    if spended_percent:
                        availible_budget_data += f" ({spended_percent}%)"
                else:
                    availible_budget_data = f"Overrun {budget_balanse:.2f}"

                sections.append(
                    formatting.as_key_value(f"{symbol} {budget.name}", f"{budget_data} ({availible_budget_data})\n")
                )

            else:
                spent = budget.spent if budget.spent else 0
                budget_data = f"{spent:.2f} / {budget.limit:.2f}"
                if budget.limit:
                    spended_percent = int((spent / budget.limit) * 100)
                    budget_data += f" ({spended_percent}%)"
                symbol = "✅" if budget.limit and spent <= budget.limit else "❌"
                sections.append(formatting.as_key_value(f"{symbol} {budget.name}", budget_data + "\n"))

        return sections

    async def _get_transactions_sum_by_budget(
        self,
        client: FireflyClient,
        budget_name: str,
        start_dttm: datetime | None = None,
        end_dttm: datetime | None = None,
    ) -> float:
        """
        Asynchronously calculates the sum of transaction amounts for a specific budget based on the provided criteria.

        Parameters:
            client (FireflyClient): The Firefly client used to retrieve transactions.
            budget_name (str): The name of the budget to calculate the sum for.
            start_dttm (Optional[datetime], optional): The start datetime for the transactions. Defaults to None.
            end_dttm (Optional[datetime], optional): The end datetime for the transactions. Defaults to None.

        Returns:
            float: The total sum of transaction amounts that match the specified budget name.
        """
        transactions = await client.get_transactions(start_dttm=start_dttm, end_dttm=end_dttm)
        return sum(transaction.amount or 0 for transaction in transactions if transaction.budget_name == budget_name)

    async def get_transactions(
        self,
        client: FireflyClient,
        transaction_type: TransactionType,
        start_dttm: datetime | None = None,
        end_dttm: datetime | None = None,
    ) -> list[formatting.Text]:
        """
        Asynchronously retrieves transactions based on the specified criteria and returns a list of formatted text sections.

        Args:
            client (FireflyClient): The Firefly client used to retrieve transactions.
            transaction_type (TransactionType): The type of transaction to retrieve.
            start_dttm (Optional[datetime], optional): The start datetime for the transactions. Defaults to None.
            end_dttm (Optional[datetime], optional): The end datetime for the transactions. Defaults to None.

        Returns:
            list[formatting.Text]: A list of formatted text sections representing the retrieved transactions.
                Each section contains the transaction details in the format:
                "[source_name] category_name (budget_name)
                amount (description)
        """
        sections = []
        if start_dttm is None:
            start_dttm = self.start_dttm
        if end_dttm is None:
            end_dttm = self.end_dttm
        transactions = await client.get_transactions(
            start_dttm=start_dttm, end_dttm=end_dttm, transaction_type=transaction_type
        )

        for transaction in transactions:
            description = transaction.description
            source_name = transaction.source_name
            budget_name = transaction.budget_name
            category_name = transaction.category_name
            amount = transaction.amount

            name = f"[{source_name}] {category_name} ({budget_name})"
            value = f"{amount:.2f} ({description})\n"
            sections.append(formatting.as_key_value(name, value))

        return sections

    async def get_categories(self, client: FireflyClient, exclude: list[str] | None = None) -> list[formatting.Text]:
        """
        Asynchronously retrieves categories based on the specified time range and excludes categories specified in the exclude list.

        Args:
            client (FireflyClient): The client used to retrieve categories.
            exclude (Optional[list[str]]): A list of categories to exclude from the result. Defaults to None.

        Returns:
            list[formatting.Text]: A list of sections containing the retrieved categories. Each section contains the category name and the spent and earned amounts.

        """
        if exclude is None:
            exclude = []
        sections = []
        categories = await client.get_categories(start_dttm=self.start_dttm, end_dttm=self.end_dttm)

        period_length = (self.end_dttm - self.start_dttm) + timedelta(days=1)
        last_period_start_dttm = self.start_dttm - period_length
        last_period_end_dttm = self.end_dttm - period_length
        last_period_categories = await client.get_categories(
            start_dttm=last_period_start_dttm, end_dttm=last_period_end_dttm
        )
        last_period_categories_dict = {category.name: category for category in last_period_categories}

        categories.sort(key=lambda x: x.spent.sum or 0 if x.spent else 0, reverse=False)
        sections.append(formatting.as_section(formatting.Bold("🟢 Categories: 🟢\n")))
        for category in categories:
            if category.name in exclude:
                continue
            spent = category.spent.sum if category.spent else 0
            if spent is None or spent == 0:
                continue
            last_period_operation = last_period_categories_dict.get(category.name)
            value = f"-{(spent * -1):.2f}"

            delta = (
                spent - (last_period_operation.spent.sum or 0)
                if last_period_operation and last_period_operation.spent is not None
                else spent
            )
            value += f" (📉 {delta:.2f})" if delta > 0 else f" (📈 {delta:.2f})"
            sections.append(formatting.as_key_value(f"{category.name}", value + "\n"))
        return sections


class MonthlyReport(BaseReport):
    async def generate(self, client: FireflyClient) -> formatting.Text:
        """
        Asynchronously generates a report using the provided client.

        Args:
            self: The current object instance.
            client (FireflyClient): The client used to generate the report.

        Returns:
            formatting.Text: The generated report.
        """
        settings = get_settings()
        sections = [formatting.as_section(formatting.Bold(f"📋 {self.header}"))]
        summary = await self.get_summary(client=client, add_division=True)
        sections.extend(summary)

        sections.append(formatting.Text("\n"))
        budgets = await self.get_budgets(client=client, exclude=settings.monthly_report.exclude_budgets)
        sections.extend(budgets)

        sections.append(formatting.Text("\n"))
        categories = await self.get_categories(client=client, exclude=settings.monthly_report.exclude_categories)
        sections.extend(categories)

        return formatting.as_section(*sections)


class DaylyReport(BaseReport):
    async def generate(self, client: FireflyClient) -> formatting.Text:
        """
        Asynchronously generates a report using the provided client.

        Args:
            client (FireflyClient): The client used to generate the report.

        Returns:
            formatting.Text: The generated report.
        """
        settings = get_settings()
        sections = [formatting.as_section(formatting.Bold(f"📋 {self.header}"))]
        budgets = await self.get_budgets(
            client=client,
            exclude=settings.daily_report.exclude_budgets,
            add_periodic_spent=True,
            accumulate_limit=True,
        )
        sections.extend(budgets)
        sections.append(formatting.Text("\n"))

        withdrawals = await self.get_transactions(client=client, transaction_type=TransactionType.WITHDRAWAL)
        if withdrawals:
            sections.append(formatting.as_section(formatting.Bold("🟢 Transactions: WITHDRAWAL")))
            sections.extend(withdrawals)

        deposits = await self.get_transactions(client=client, transaction_type=TransactionType.DEPOSIT)
        if deposits:
            sections.append(formatting.as_section(formatting.Bold("🟢 Transactions: DEPOSIT")))
            sections.extend(deposits)

        transfers = await self.get_transactions(client=client, transaction_type=TransactionType.TRANSFER)
        if transfers:
            sections.append(formatting.as_section(formatting.Bold("🟢 Transactions: TRANSFER")))
            sections.extend(transfers)

        return formatting.as_section(*sections)


class LastNDaysReport(BaseReport):
    async def generate(self, client: FireflyClient) -> formatting.Text:
        """
        Asynchronously generates a report using the provided client.

        Args:
            client (FireflyClient): The client used to generate the report.

        Returns:
            formatting.Text: The generated report.
        """
        settings = get_settings()
        sections = [formatting.as_section(formatting.Bold(f"📋 {self.header}"))]
        budgets = await self.get_budgets(
            client=client,
            exclude=settings.periodic_report.exclude_budgets,
            add_periodic_spent=True,
            accumulate_limit=False,
        )
        sections.extend(budgets)

        sections.append(formatting.Text("\n"))
        categories = await self.get_categories(client=client, exclude=settings.periodic_report.exclude_categories)
        sections.extend(categories)

        return formatting.as_section(*sections)


def get_reports() -> Sequence[BaseReport]:
    """
    Retrieves a list of reports based on the current settings.

    Returns:
        Sequence[BaseReport]: A list of reports to be generated. Each report is an instance of the BaseReport class.
            The reports include:
            - Daily report: Generated if the daily report setting is enabled and the current date is not the first day of the month.
            - Monthly report: Generated if the monthly report setting is enabled and the current date is the first day of the month.
            - Last N days report: Generated if the periodic report setting is enabled, the current date is not the first day of the month,
              and the current date minus the day period is a multiple of the day period.

    """
    settings = get_settings()
    current_date = datetime.now()
    yesterday = current_date - timedelta(days=1)
    reports: list[BaseReport] = []
    if settings.daily_report.send_report:
        reports.append(
            DaylyReport(
                header=f"Daily report: {yesterday.strftime('%Y-%m-%d')}",
                start_dttm=yesterday.replace(hour=0, minute=0, second=0),
                end_dttm=yesterday.replace(hour=23, minute=59, second=59),
            )
        )
    if settings.monthly_report.send_report and current_date.day == 1:
        reports.append(
            MonthlyReport(
                header=f"Monthly report: {yesterday.strftime('%Y-%m')}",
                start_dttm=yesterday.replace(day=1, hour=0, minute=0, second=0),
                end_dttm=yesterday.replace(hour=23, minute=59, second=59),
            )
        )

    if (
        settings.periodic_report.send_report
        and current_date.day != 1
        and (current_date.day - 1) % settings.day_period == 0
    ):
        start_dttm = (current_date - timedelta(days=settings.day_period)).replace(hour=0, minute=0, second=0)
        end_dttm = yesterday.replace(hour=23, minute=59, second=59)
        reports.append(
            LastNDaysReport(
                header=f"Last {settings.day_period} days report: {start_dttm.strftime('%Y-%m')} {start_dttm.day}-{end_dttm.day}",
                start_dttm=start_dttm,
                end_dttm=end_dttm,
            )
        )
    return reports
