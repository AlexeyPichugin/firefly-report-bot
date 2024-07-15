from datetime import datetime
from pydantic import BaseModel, Field
from firefly_report_bot.client.models.base import BaseAttributes, BaseFireflyModel, BaseData
from firefly_report_bot.client.enums import TransactionTypeProperty, AccountTypeProperty


class TransactionSplit(BaseModel):
    """
    Represents a transaction split.

    Attributes:
        user (str): The ID of the user.
        transaction_journal_id (str): The ID of the transaction journal.
        type (TransactionTypeProperty): The type of the transaction.
        date (str): The date of the transaction.
        order (int, optional): The order of the transaction.
        currency_id (str, optional): The ID of the currency.
        currency_code (str, optional): The code of the currency.
        currency_symbol (str): The symbol of the currency.
        currency_name (str): The name of the currency.
        currency_decimal_places (int): The number of decimal places for the currency.
        foreign_currency_id (str, optional): The ID of the foreign currency.
        foreign_currency_code (str, optional): The code of the foreign currency.
        foreign_currency_symbol (str, optional): The symbol of the foreign currency.
        foreign_currency_decimal_places (int, optional): The number of decimal places for the foreign currency.
        amount (str): The amount of the transaction.
        foreign_amount (str, optional): The foreign amount of the transaction.
        description (str): The description of the transaction.
        source_id (str, optional): The ID of the source account.
        source_name (str, optional): The name of the source account.
        source_iban (str, optional): The IBAN of the source account.
        source_type (AccountTypeProperty, optional): The type of the source account.
        destination_id (str, optional): The ID of the destination account.
        destination_name (str, optional): The name of the destination account.
        destination_iban (str, optional): The IBAN of the destination account.
        destination_type (AccountTypeProperty, optional): The type of the destination account.
        budget_id (str, optional): The ID of the budget.
        budget_name (str, optional): The name of the budget.
        category_id (str, optional): The ID of the category.
        category_name (str, optional): The name of the category.
        bill_id (str, optional): The ID of the bill.
        bill_name (str, optional): The name of the bill.
        reconciled (bool): Whether the transaction is reconciled.
        notes (str, optional): The notes for the transaction.
        tags (list[str]): The tags for the transaction.
        internal_reference (str, optional): The internal reference for the transaction.
        external_id (str, optional): The external ID for the transaction.
        external_url (str, optional): The external URL for the transaction.
        original_source (str, optional): The original source for the transaction.
        recurrence_id (str, optional): The ID of the recurrence.
        recurrence_total (int, optional): The total number of recurrences.
        recurrence_count (int, optional): The count of recurrences.
        bunq_payment_id (str, optional): The ID of the bunq payment.
        import_hash_v2 (str, optional): The import hash for the transaction.
        sepa_cc (str, optional): The SEPA credit card for the transaction.
        sepa_ct_op (str, optional): The SEPA credit transfer operation for the transaction.
        sepa_ct_id (str, optional): The SEPA credit transfer ID for the transaction.
        sepa_db (str, optional): The SEPA debit bank for the transaction.
        sepa_country (str, optional): The SEPA country for the transaction.
        sepa_ep (str, optional): The SEPA end-to-end protection for the transaction.
        sepa_ci (str, optional): The SEPA correlation ID for the transaction.
        sepa_batch_id (str, optional): The SEPA batch ID for the transaction.
        interestdate (datetime, optional): The date of the interest.
        bookdate (datetime, optional): The book date of the transaction.
        processdate (datetime, optional): The process date of the transaction.
        duedate (datetime, optional): The due date of the transaction.
        paymentdate (datetime, optional): The payment date of the transaction.
        invoicedate (datetime, optional): The invoice date of the transaction.
        latitude (float, optional): The latitude of the transaction.
        longitude (float, optional): The longitude of the transaction.
        zoom_level (int, optional): The zoom level of the transaction.
        has_attachments (bool): Whether the transaction has attachments.
    """

    user: str
    transaction_journal_id: int
    type: TransactionTypeProperty
    date: datetime
    order: int | None = None
    currency_id: int | None = None
    currency_code: str | None = None
    currency_symbol: str
    currency_name: str
    currency_decimal_places: int
    foreign_currency_id: int | None = None
    foreign_currency_code: str | None = None
    foreign_currency_symbol: str | None = None
    foreign_currency_decimal_places: int | None = None
    amount: float
    foreign_amount: str | None = None
    description: str
    source_id: int | None = None
    source_name: str | None = None
    source_iban: str | None = None
    source_type: AccountTypeProperty | None = Field(None)
    destination_id: int | None = None
    destination_name: str | None = None
    destination_iban: str | None = None
    destination_type: AccountTypeProperty | None = Field(None)
    budget_id: int | None = None
    budget_name: str | None = None
    category_id: int | None = None
    category_name: str | None = None
    bill_id: int | None = None
    bill_name: str | None = None
    reconciled: bool
    notes: str | None = None
    tags: list[str] = Field(..., default_factory=list)
    internal_reference: str | None = None
    external_id: int | None = None
    external_url: str | None = None
    original_source: str | None = None
    recurrence_id: int | None = None
    recurrence_total: int | None = None
    recurrence_count: int | None = None
    bunq_payment_id: int | None = None
    import_hash_v2: str | None = None
    sepa_cc: str | None = None
    sepa_ct_op: str | None = None
    sepa_ct_id: int | None = None
    sepa_db: str | None = None
    sepa_country: str | None = None
    sepa_ep: str | None = None
    sepa_ci: str | None = None
    sepa_batch_id: int | None = None
    interestdate: datetime | None = None
    bookdate: datetime | None = None
    processdate: datetime | None = None
    duedate: datetime | None = None
    paymentdate: datetime | None = None
    invoicedate: datetime | None = None
    latitude: float | None = None
    longitude: float | None = None
    zoom_level: int | None = None
    has_attachments: bool


class TransactionAttributes(BaseAttributes):
    """
    Attributes for a transaction.

    Attributes:
        created_at (datetime | None): The datetime when the transaction was created.
        updated_at (datetime | None): The datetime when the transaction was last updated.
        user (str): The user associated with the transaction.
        group_title (str | None): The title of the group the transaction belongs to.
        transactions (list[TransactionSplit]): The list of transaction splits.
    """

    created_at: datetime | None = None
    updated_at: datetime | None = None
    user: str
    group_title: str | None = None
    transactions: list[TransactionSplit] = Field(..., default_factory=list)


class TransactionData(BaseData):
    """
    Class representing the data of a transaction.

    Attributes:
        attributes (TransactionAttributes): The attributes of the transaction.
    """

    attributes: TransactionAttributes


class TransactionModel(BaseFireflyModel):
    """
    Class representing a transaction.

    Attributes:
        data (TransactionData): The data of the transaction.
    """

    data: TransactionData


class TransactionsModel(BaseFireflyModel):
    """
    Class representing a collection of transaction data.

    Attributes:
        data (list[TransactionData]): A list of transaction data.
    """

    data: list[TransactionData]
