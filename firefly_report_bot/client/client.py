import httpx
import typing
from urllib.parse import urljoin
from httpx._client import UseClientDefault, USE_CLIENT_DEFAULT
from httpx._types import (
    RequestData,
    RequestFiles,
    RequestExtensions,
    RequestContent,
    AuthTypes,
    CookieTypes,
    HeaderTypes,
    QueryParamTypes,
    TimeoutTypes,
)

from datetime import datetime
from loguru import logger

from firefly_report_bot.config import FireflyClientSettings
from firefly_report_bot.client.models.base import MetadataPagination, Metadata
from firefly_report_bot.client.enums import TransactionType, AccountType
from firefly_report_bot.client.models.accounts import AccountAttributes, AccountModel, AccountsModel
from firefly_report_bot.client.models.budgets import (
    BudgetAttributes,
    BudgetModel,
    BudgetsModel,
    BudgetLimitsModel,
    BudgetLimitAttrebutes,
    BudgetTransactionsModel,
)
from firefly_report_bot.client.models.categories import CategoryAttributes, CategoryModel, CategoriesModel
from firefly_report_bot.client.models.transactions import TransactionAttributes, TransactionModel, TransactionsModel
from firefly_report_bot.client.classes import (
    Transaction,
    Budget,
    Category,
    Account,
)


class FireflyClient:
    def __init__(self, settings: FireflyClientSettings):
        """
        Constructor for the FireflyClient class.
        Initializes the URL and token attributes using environment variables FIREFLY_URL and FIREFLY_TOKEN.
        """
        self.url = urljoin(settings.api_url, "/api/v1/")
        self.token = settings.api_key
        self.timeout = settings.request_timeout
        if self.url is None or self.token is None:
            raise ValueError("FIREFLY_URL and FIREFLY_TOKEN must be set in the environment")

    async def _make_request(
        self,
        method: str,
        path: str,
        content: RequestContent | None = None,
        data: RequestData | None = None,
        files: RequestFiles | None = None,
        json: typing.Any | None = None,
        params: QueryParamTypes | None = None,
        headers: HeaderTypes | None = None,
        cookies: CookieTypes | None = None,
        auth: AuthTypes | UseClientDefault | None = USE_CLIENT_DEFAULT,
        follow_redirects: bool | UseClientDefault = USE_CLIENT_DEFAULT,
        timeout: TimeoutTypes | UseClientDefault = USE_CLIENT_DEFAULT,
        extensions: RequestExtensions | None = None,
    ) -> httpx.Response | None:
        """
        Asynchronously makes a request to the Firefly API with the given parameters.

        Args:
            method (str): The HTTP method to use for the request.
            path (str): The path of the API endpoint to request.
            content (RequestContent | None, optional): The request content. Defaults to None.
            data (RequestData | None, optional): The request data. Defaults to None.
            files (RequestFiles | None, optional): The request files. Defaults to None.
            json (typing.Any | None, optional): The JSON data to send in the request body. Defaults to None.
            params (QueryParamTypes | None, optional): The query parameters to include in the request URL. Defaults to None.
            headers (HeaderTypes | None, optional): The headers to include in the request. Defaults to None.
            cookies (CookieTypes | None, optional): The cookies to include in the request. Defaults to None.
            auth (AuthTypes | UseClientDefault | None, optional): The authentication credentials to use for the request. Defaults to USE_CLIENT_DEFAULT.
            follow_redirects (bool | UseClientDefault, optional): Whether to follow redirects. Defaults to USE_CLIENT_DEFAULT.
            timeout (TimeoutTypes | UseClientDefault, optional): The timeout for the request. Defaults to USE_CLIENT_DEFAULT.
            extensions (RequestExtensions | None, optional): The request extensions. Defaults to None.

        Returns:
            Returns an httpx.Response object if successful, otherwise None.
        """

        async with httpx.AsyncClient(
            base_url=self.url, headers={"Authorization": f"Bearer {self.token}"}, timeout=self.timeout
        ) as client:
            try:
                response = await client.request(
                    method=method,
                    url=path,
                    content=content,
                    data=data,
                    files=files,
                    json=json,
                    params=params,
                    headers=headers,
                    cookies=cookies,
                    auth=auth,
                    follow_redirects=follow_redirects,
                    timeout=timeout,
                    extensions=extensions,
                )
                response.raise_for_status()
                return response
            except httpx.RequestError as e:
                logger.error(e)
                return None
            except httpx.HTTPStatusError as e:
                logger.error(e)
                return None
            except Exception as e:
                logger.exception(e)
                return None

    async def _get_accounts(
        self, dttm: datetime | None = None, account_type: AccountType = AccountType.ALL
    ) -> dict[int, AccountAttributes]:
        """
        A function to get accounts based on the specified date and account type.

        Args:
            dttm (datetime | None, optional): The datetime to filter the accounts. Defaults to None.
            account_type (AccountType, optional): The type of accounts to retrieve. Defaults to AccountType.ALL.

        Returns:
            dict[int, AccountAttributes]: A dictionary containing account IDs as keys and their attributes as values.
        """

        async def _get_accounts(
            dttm: datetime | None = None, account_type: AccountType = AccountType.ALL, page: int = 1
        ) -> AccountsModel:
            params = {"page": page, "type": account_type.value}
            if dttm is not None:
                params["date"] = dttm.strftime("%Y-%m-%d")
            resp = await self._make_request("GET", "/accounts", params=params)
            if resp is None:
                return AccountsModel(data=[], meta=Metadata(pagination=MetadataPagination(total_pages=0)))
            return AccountsModel.model_validate(resp.json())

        accounts = await _get_accounts(dttm=dttm, account_type=account_type)
        result = {account.id: account.attributes for account in accounts.data}
        for page in range(2, accounts.meta.pagination.total_pages + 1):
            accounts = await _get_accounts(dttm=dttm, account_type=account_type, page=page)
            result.update({account.id: account.attributes for account in accounts.data})
        return result

    async def _get_account_by_id(self, account_id: int, dttm: datetime | None = None) -> AccountAttributes | None:
        """
        A function to get an account by ID.

        Args:
            account_id (str): The ID of the account to retrieve.
            dttm (datetime | None, optional): The datetime to filter the account. Defaults to None.

        Returns:
            AccountAttributes: The attributes of the retrieved account.
        """
        params = {}
        if dttm is not None:
            params["date"] = dttm.strftime("%Y-%m-%d")
        resp = await self._make_request("GET", f"/accounts/{account_id}", params=params)
        if resp is None:
            return None
        account = AccountModel.model_validate(resp.json())
        return account.data.attributes

    async def _get_budgets(
        self, start_dttm: datetime | None = None, end_dttm: datetime | None = None
    ) -> dict[int, BudgetAttributes]:
        """
        A function to get budgets within a specified time range.

        Args:
            start_dttm (datetime | None, optional): The start datetime of the range. Defaults to None.
            end_dttm (datetime | None, optional): The end datetime of the range. Defaults to None.

        Returns:
            dict[int, BudgetAttributes]: A dictionary containing budget IDs as keys and their attributes as values.
        """

        async def __get_budgets(
            start_dttm: datetime | None = None, end_dttm: datetime | None = None, page: int = 1
        ) -> BudgetsModel:
            params: dict[str, typing.Any] = {"page": page}
            if start_dttm is not None:
                params["start"] = start_dttm.strftime("%Y-%m-%d")
            if end_dttm is not None:
                params["end"] = end_dttm.strftime("%Y-%m-%d")
            resp = await self._make_request("GET", "/budgets", params=params)
            if resp is None:
                return BudgetsModel(data=[], meta=Metadata(pagination=MetadataPagination(total_pages=0)))
            return BudgetsModel.model_validate(resp.json())

        budgets = await __get_budgets(start_dttm=start_dttm, end_dttm=end_dttm)
        result = {budget.id: budget.attributes for budget in budgets.data}
        for page in range(2, budgets.meta.pagination.total_pages + 1):
            budgets = await __get_budgets(start_dttm=start_dttm, end_dttm=end_dttm, page=page)
            result.update({budget.id: budget.attributes for budget in budgets.data})
        return result

    async def _get_budget_by_id(
        self, budget_id: int, start_dttm: datetime | None = None, end_dttm: datetime | None = None
    ) -> BudgetAttributes | None:
        """
        Asynchronously retrieves a budget by its ID within a specified time range.

        Args:
            budget_id (str): The ID of the budget to retrieve.
            start_dttm (datetime | None, optional): The start datetime of the range. Defaults to None.
            end_dttm (datetime | None, optional): The end datetime of the range. Defaults to None.

        Returns:
            BudgetAttributes: The attributes of the retrieved budget.
        """

        params = {}
        if start_dttm is not None:
            params["start"] = start_dttm.strftime("%Y-%m-%d")
        if end_dttm is not None:
            params["end"] = end_dttm.strftime("%Y-%m-%d")
        resp = await self._make_request("GET", f"/budgets/{budget_id}", params=params)
        if resp is None:
            return None
        budget = BudgetModel.model_validate(resp.json())
        return budget.data.attributes

    async def _get_budget_limits(
        self, start_dttm: datetime | None = None, end_dttm: datetime | None = None
    ) -> dict[int, BudgetLimitAttrebutes]:
        """
        A function to retrieve budget limits within a specified time range.

        Args:
            start_dttm (datetime | None, optional): The start datetime of the range. Defaults to None.
            end_dttm (datetime | None, optional): The end datetime of the range. Defaults to None.

        Returns:
            dict[int, BudgetLimitAttrebutes]: A dictionary containing budget limit IDs as keys and their attributes as values.
        """

        params = {}
        if start_dttm is not None:
            params["start"] = start_dttm.strftime("%Y-%m-%d")
        if end_dttm is not None:
            params["end"] = end_dttm.strftime("%Y-%m-%d")
        resp = await self._make_request("GET", "/budget-limits", params=params)
        if not resp:
            return {}
        budget_limits = BudgetLimitsModel.model_validate(resp.json())
        return {limit.id: limit.attributes for limit in budget_limits.data}

    async def _get_budget_transactions(
        self,
        id: int,
        start_dttm: datetime | None = None,
        end_dttm: datetime | None = None,
        transaction_type: TransactionType = TransactionType.ALL,
    ) -> dict[int, TransactionAttributes]:
        """
        Asynchronously retrieves budget transactions based on the specified criteria and returns a dictionary with transaction IDs as keys and their attributes as values.

        Args:
            id (int): The ID of the budget.
            start_dttm (Optional[datetime], optional): The start datetime for the transactions. Defaults to None.
            end_dttm (Optional[datetime], optional): The end datetime for the transactions. Defaults to None.
            transaction_type (TransactionType, optional): The type of transaction to retrieve. Defaults to TransactionType.ALL.

        Returns:
            dict[int, TransactionAttributes]: A dictionary containing transaction IDs as keys and their attributes as values.
        """

        async def __get_butget_transactions(
            id: int,
            start_dttm: datetime | None = None,
            end_dttm: datetime | None = None,
            transaction_type: TransactionType = TransactionType.ALL,
            page: int = 1,
        ) -> BudgetTransactionsModel:
            params = {"page": page, "type": transaction_type.value}
            if start_dttm is not None:
                params["start"] = start_dttm.strftime("%Y-%m-%d")
            if end_dttm is not None:
                params["end"] = end_dttm.strftime("%Y-%m-%d")
            resp = await self._make_request("GET", f"/budgets/{id}/transactions", params=params)
            if resp is None:
                return BudgetTransactionsModel(data=[], meta=Metadata(pagination=MetadataPagination(total_pages=0)))
            return BudgetTransactionsModel.model_validate(resp.json())

        transactions = await __get_butget_transactions(
            id=id, start_dttm=start_dttm, end_dttm=end_dttm, transaction_type=transaction_type
        )
        result = {transaction.id: transaction.attributes for transaction in transactions.data}
        for page in range(2, transactions.meta.pagination.total_pages + 1):
            transactions = await __get_butget_transactions(
                id=id, start_dttm=start_dttm, end_dttm=end_dttm, transaction_type=transaction_type, page=page
            )
            result.update({transaction.id: transaction.attributes for transaction in transactions.data})
        return result

    async def _get_categories(self) -> dict[int, CategoryAttributes]:
        """
        Retrieves all categories from the API, paginating through the results if necessary.

        Returns:
            dict[int, CategoryAttributes]: A dictionary mapping category IDs to their attributes.
        """

        async def __get_categories(page: int = 1) -> CategoriesModel:
            params = {"page": page}
            resp = await self._make_request("GET", "/categories", params=params)
            if resp is None:
                return CategoriesModel(data=[], meta=Metadata(pagination=MetadataPagination(total_pages=0)))
            return CategoriesModel.model_validate(resp.json())

        categories = await __get_categories()
        result = {category.id: category.attributes for category in categories.data}
        for page in range(2, categories.meta.pagination.total_pages + 1):
            categories = await __get_categories(page=page)
            result.update({category.id: category.attributes for category in categories.data})
        return result

    async def _get_category_by_id(
        self, category_id: int, start_dttm: datetime | None = None, end_dttm: datetime | None = None
    ) -> CategoryAttributes | None:
        """
        Asynchronously retrieves a category by its ID within a specified time range.

        Args:
            category_id (int): The ID of the category to retrieve.
            start_dttm (datetime | None, optional): The start datetime of the range. Defaults to None.
            end_dttm (datetime | None, optional): The end datetime of the range. Defaults to None.

        Returns:
            CategoryAttributes | None: The attributes of the retrieved category, or None if the request failed.
        """

        params = {}
        if start_dttm is not None:
            params["start"] = start_dttm.strftime("%Y-%m-%d")
        if end_dttm is not None:
            params["end"] = end_dttm.strftime("%Y-%m-%d")
        resp = await self._make_request("GET", f"/categories/{category_id}", params=params)
        if resp is None:
            return None
        category = CategoryModel.model_validate(resp.json())
        return category.data.attributes

    async def _get_transactions(
        self,
        start_dttm: datetime | None = None,
        end_dttm: datetime | None = None,
        transaction_type: TransactionType = TransactionType.ALL,
    ) -> dict[int, TransactionAttributes]:
        """
        Retrieves transactions asynchronously based on the specified criteria and returns a dictionary with transaction IDs as keys and attributes as values.

        Parameters:
            start_dttm (Optional[datetime]): The start datetime for the transactions.
            end_dttm (Optional[datetime]): The end datetime for the transactions.
            transaction_type (TransactionType): The type of transaction to retrieve.

        Returns:
            dict[int, TransactionAttributes]: A dictionary containing transaction IDs as keys and their attributes as values.
        """

        async def __get_transactions(
            start_dttm: datetime | None = None,
            end_dttm: datetime | None = None,
            transaction_type: TransactionType = TransactionType.ALL,
            page: int = 1,
        ) -> TransactionsModel:
            params = {"page": page, "type": transaction_type.value}
            if start_dttm is not None:
                params["start"] = start_dttm.strftime("%Y-%m-%d")
            if end_dttm is not None:
                params["end"] = end_dttm.strftime("%Y-%m-%d")
            resp = await self._make_request("GET", "/transactions", params=params)
            if resp is None:
                return TransactionsModel(data=[], meta=Metadata(pagination=MetadataPagination(total_pages=0)))
            return TransactionsModel.model_validate(resp.json())

        transactions = await __get_transactions(
            start_dttm=start_dttm, end_dttm=end_dttm, transaction_type=transaction_type
        )
        result = {transaction.id: transaction.attributes for transaction in transactions.data}
        for page in range(2, transactions.meta.pagination.total_pages + 1):
            transactions = await __get_transactions(
                start_dttm=start_dttm, end_dttm=end_dttm, transaction_type=transaction_type, page=page
            )
            result.update({transaction.id: transaction.attributes for transaction in transactions.data})
        return result

    async def _get_transaction_by_id(
        self, transaction_id: int, start_dttm: datetime | None = None, end_dttm: datetime | None = None
    ) -> TransactionAttributes | None:
        """
        Asynchronously retrieves a transaction by its ID within a specified time range.

        Args:
            transaction_id (str): The ID of the transaction to retrieve.
            start_dttm (Optional[datetime]): The start datetime of the range. Defaults to None.
            end_dttm (Optional[datetime]): The end datetime of the range. Defaults to None.

        Returns:
            TransactionAttributes: The attributes of the retrieved transaction.
        """

        params = {}
        if start_dttm is not None:
            params["start"] = start_dttm.strftime("%Y-%m-%d")
        if end_dttm is not None:
            params["end"] = end_dttm.strftime("%Y-%m-%d")
        resp = await self._make_request("GET", f"/transactions/{transaction_id}", params=params)
        if resp is None:
            return None
        transaction = TransactionModel.model_validate(resp.json())
        return transaction.data.attributes

    async def get_categories(
        self,
        start_dttm: datetime | None = None,
        end_dttm: datetime | None = None,
    ) -> list[Category]:
        """
        Asynchronously retrieves categories based on the specified time range.

        Args:
            start_dttm (Optional[datetime]): The start datetime of the range. Defaults to None.
            end_dttm (Optional[datetime]): The end datetime of the range. Defaults to None.

        Returns:
            list[Category]: A list of Category objects representing the retrieved categories.
        """

        result: list[Category] = []
        categories = await self._get_categories()

        for id in categories.keys():
            category_attributes = await self._get_category_by_id(id, start_dttm=start_dttm, end_dttm=end_dttm)
            if category_attributes is None:
                continue
            result.append(Category.from_category_attributes(category_attributes))
        return result

    async def get_budgets(
        self,
        start_dttm: datetime | None = None,
        end_dttm: datetime | None = None,
    ) -> list[Budget]:
        """
        Asynchronously retrieves a list of Budget objects within a specified time range.

        Args:
            start_dttm (datetime | None, optional): The start datetime of the range. Defaults to None.
            end_dttm (datetime | None, optional): The end datetime of the range. Defaults to None.

        Returns:
            list[Budget]: A list of Budget objects representing the retrieved budgets.
        """

        result: list[Budget] = []
        budgets = await self._get_budgets(start_dttm, end_dttm)
        budget_limits = await self._get_budget_limits(start_dttm, end_dttm)
        for id in budgets.keys():
            budget_attributes = budgets[id]
            if budget_attributes.active is False:
                continue
            budget_limits_attributes = None
            for budget_limit in budget_limits.values():
                if budget_limit.budget_id == id:
                    budget_limits_attributes = budget_limit
            budget_transactions = await self._get_budget_transactions(id=id, start_dttm=start_dttm, end_dttm=end_dttm)
            result.append(
                Budget.from_budget_attributes(
                    budget_attributes=budget_attributes,
                    budget_limit_attributes=budget_limits_attributes,
                    budget_transactions=list(budget_transactions.values()),
                )
            )
        return result

    async def get_transactions(
        self,
        start_dttm: datetime | None = None,
        end_dttm: datetime | None = None,
        transaction_type: TransactionType = TransactionType.ALL,
    ) -> list[Transaction]:
        """
        Retrieves transactions asynchronously based on the specified criteria and returns a list of Transaction objects.

        Parameters:
            start_dttm (Optional[datetime]): The start datetime for the transactions.
            end_dttm (Optional[datetime]): The end datetime for the transactions.
            transaction_type (TransactionType): The type of transaction to retrieve.

        Returns:
            list[Transaction]: A list of Transaction objects representing the retrieved transactions.
        """

        result: list[Transaction] = []
        transactions = await self._get_transactions(start_dttm, end_dttm, transaction_type)
        for id in transactions.keys():
            transaction_attributes = transactions[id]
            transaction = Transaction.from_transaction_attributes(transaction_attributes)
            if transaction is None:
                continue
            result.append(transaction)
        return result

    async def get_accounts(
        self, dttm: datetime | None = None, account_type: AccountType = AccountType.ALL
    ) -> list[Account]:
        """
        Retrieves accounts asynchronously based on the specified criteria and returns a list of Account objects.

        Parameters:
            self: The FireflyClient instance.
            dttm (Optional[datetime]): The datetime to filter the accounts. Defaults to None.
            account_type (AccountType): The type of accounts to retrieve. Defaults to AccountType.ALL.

        Returns:
            list[Account]: A list of Account objects representing the retrieved accounts.
        """
        result: list[Account] = []
        accounts = await self._get_accounts(dttm=dttm, account_type=account_type)
        for account_attributes in accounts.values():
            result.append(Account.from_account_attributes(account_attributes))
        return result
