from enum import Enum


class FireflyAccountType(Enum):
    """
    Enum representing the different types of accounts.

    Attributes:
        ASSET (str): Represents an asset account.
        EXPENSE (str): Represents an expense account.
        IMPORT (str): Represents an import account.
        REVENUE (str): Represents a revenue account.
        CASH (str): Represents a cash account.
        LIABILITY (str): Represents a liability account.
        LIABILITIES (str): Represents liabilities accounts.
        INITIAL_BALANCE (str): Represents an initial balance account.
        RECONCILIATION (str): Represents a reconciliation account.
    """

    ASSET = "asset"
    EXPENSE = "expense"
    IMPORT = "import"
    REVENUE = "revenue"
    CASH = "cash"
    LIABILITY = "liability"
    LIABILITIES = "liabilities"
    INITIAL_BALANCE = "initial-balance"
    RECONCILIATION = "reconciliation"


class AccountRole(Enum):
    """
    Enum representing the different roles of accounts.

    Attributes:
        DEFAULT_ASSET (str): The default asset account.
        SHARED_ASSET (str): A shared asset account.
        SAVING_ASSET (str): A saving asset account.
        CC_ASSET (str): A credit card asset account.
        CASH_WALLET_ASSET (str): A cash wallet asset account.
    """

    DEFAULT_ASSET = "defaultAsset"
    SHARED_ASSET = "sharedAsset"
    SAVING_ASSET = "savingAsset"
    CC_ASSET = "ccAsset"
    CASH_WALLET_ASSET = "cashWalletAsset"


class CreditCardType(Enum):
    """
    Enum representing the different types of credit cards.

    Attributes:
        MONTHLY_FULL (str): A credit card that is paid in full each month.
    """

    MONTHLY_FULL = "monthlyFull"


class LiabilityType(Enum):
    """
    Enum representing the different types of liabilities.

    Attributes:
        LOAN (str): A loan liability.
        DEBT (str): A debt liability.
        MORTGAGE (str): A mortgage liability.
    """

    LOAN = "loan"
    DEBT = "debt"
    MORTGAGE = "mortgage"


class LiabilityDirection(Enum):
    """
    Enum representing the direction of a liability.

    Attributes:
        CREDIT (str): A credit liability.
        DEBIT (str): A debit liability.
    """

    CREDIT = "credit"
    DEBIT = "debit"


class InterestPeriod(Enum):
    """
    Enum representing the different periods at which interest is added to accounts.

    Attributes:
        WEEKLY (str): Interest is added weekly.
        MONTHLY (str): Interest is added monthly.
        QUARTERLY (str): Interest is added quarterly (every 3 months).
        HALF_YEAR (str): Interest is added every 6 months.
        YEARLY (str): Interest is added yearly.
    """

    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    HALF_YEAR = "half-year"
    YEARLY = "yearly"


class AutoBudgetType(Enum):
    """
    Enum representing the type of auto budget.

    Attributes:
        RESET (str): Reset the budget to zero.
        ROLLOVER (str): Roll over the budget to the next month.
        NONE (str): Do not use an auto budget.
    """

    RESET = "reset"
    ROLLOVER = "rollover"
    NONE = "none"


class AutoBudgetPeriod(Enum):
    """
    Enum representing different auto budget periods.

    Attributes:
        DAILY (str): Daily budget period.
        WEEKLY (str): Weekly budget period.
        MONTHLY (str): Monthly budget period.
        QUARTERLY (str): Quarterly budget period.
        HALF_YEAR (str): Half-year budget period.
        YEARLY (str): Yearly budget period.
    """

    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    HALF_YEAR = "half-year"
    YEARLY = "yearly"


class TransactionTypeProperty(Enum):
    """
    Enum representing different transaction types.

    Attributes:
        WITHDRAWAL (str): Withdrawal transaction type.
        DEPOSIT (str): Deposit transaction type.
        TRANSFER (str): Transfer transaction type.
        RECONCILIATION (str): Reconciliation transaction type.
        OPENING_BALANCE (str): Opening balance transaction type.
    """

    WITHDRAWAL = "withdrawal"
    DEPOSIT = "deposit"
    TRANSFER = "transfer"
    RECONCILIATION = "reconciliation"
    OPENING_BALANCE = "opening balance"


class AccountTypeProperty(Enum):
    """
    Enum representing different account types.

    Attributes:
        DEFAULT_ACCOUNT (str): Default account.
        CASH_ACCOUNT (str): Cash account.
        ASSET_ACCOUNT (str): Asset account.
        EXPENSE_ACCOUNT (str): Expense account.
        REVENUE_ACCOUNT (str): Revenue account.
        INITIAL_BALANCE_ACCOUNT (str): Initial balance account.
        BENEFICIARY_ACCOUNT (str): Beneficiary account.
        IMPORT_ACCOUNT (str): Import account.
        RECONCILIATION_ACCOUNT (str): Reconciliation account.
        LOAN (str): Loan account.
        DEBT (str): Debt account.
        MORTGAGE (str): Mortgage account.
    """

    DEFAULT_ACCOUNT = "Default account"
    CASH_ACCOUNT = "Cash account"
    ASSET_ACCOUNT = "Asset account"
    EXPENSE_ACCOUNT = "Expense account"
    REVENUE_ACCOUNT = "Revenue account"
    INITIAL_BALANCE_ACCOUNT = "Initial balance account"
    BENEFICIARY_ACCOUNT = "Beneficiary account"
    IMPORT_ACCOUNT = "Import account"
    RECONCILIATION_ACCOUNT = "Reconciliation account"
    LOAN = "Loan"
    DEBT = "Debt"
    MORTGAGE = "Mortgage"


class TransactionType(Enum):
    """
    Enum representing different transaction types.

    Attributes:
        ALL (str): All transactions.
        WITHDRAWAL (str): Withdrawal transaction.
        WITHDRAWALS (str): Multiple withdrawal transactions.
        EXPENSE (str): Expense transaction.
        DEPOSIT (str): Deposit transaction.
        DEPOSITS (str): Multiple deposit transactions.
        INCOME (str): Income transaction.
        TRANSFER (str): Transfer transaction.
        TRANSFERS (str): Multiple transfer transactions.
        OPENING_BALANCE (str): Opening balance transaction.
        RECONCILIATION (str): Reconciliation transaction.
        SPECIAL (str): Special transaction.
        SPECIALS (str): Multiple special transactions.
        DEFAULT (str): Default transaction.
    """

    ALL = "all"
    WITHDRAWAL = "withdrawal"
    WITHDRAWALS = "withdrawals"
    EXPENSE = "expense"
    DEPOSIT = "deposit"
    DEPOSITS = "deposits"
    INCOME = "income"
    TRANSFER = "transfer"
    TRANSFERS = "transfers"
    OPENING_BALANCE = "opening_balance"
    RECONCILIATION = "reconciliation"
    SPECIAL = "special"
    SPECIALS = "specials"
    DEFAULT = "default"


class AccountType(Enum):
    """
    Enum representing different types of accounts.

    Attributes:
        ALL (str): All accounts.
        ASSET (str): Asset account.
        CASH (str): Cash account.
        EXPENSE (str): Expense account.
        REVENUE (str): Revenue account.
        SPECIAL (str): Special account.
        HIDDEN (str): Hidden account.
        LIABILITY (str): Liability account.
        LIABILITIES (str): Liabilities account.
        DEFAULT_ACCOUNT (str): Default account.
        CASH_ACCOUNT (str): Cash account.
        ASSET_ACCOUNT (str): Asset account.
        EXPENSE_ACCOUNT (str): Expense account.
        REVENUE_ACCOUNT (str): Revenue account.
        INITIAL_BALANCE_ACCOUNT (str): Initial balance account.
        BENEFICIARY_ACCOUNT (str): Beneficiary account.
        IMPORT_ACCOUNT (str): Import account.
        RECONCILIATION_ACCOUNT (str): Reconciliation account.
        LOAN (str): Loan account.
        DEBT (str): Debt account.
        MORTGAGE (str): Mortgage account.
    """

    ALL = " all"
    ASSET = "asset"
    CASH = "cash"
    EXPENSE = "expense"
    REVENUE = "revenue"
    SPECIAL = "special"
    HIDDEN = "hidden"
    LIABILITY = "liability"
    LIABILITIES = "liabilities"
    DEFAULT_ACCOUNT = "Default account"
    CASH_ACCOUNT = "Cash account"
    ASSET_ACCOUNT = "Asset account"
    EXPENSE_ACCOUNT = "Expense account"
    REVENUE_ACCOUNT = "Revenue account"
    INITIAL_BALANCE_ACCOUNT = "Initial balance account"
    BENEFICIARY_ACCOUNT = "Beneficiary account"
    IMPORT_ACCOUNT = "Import account"
    RECONCILIATION_ACCOUNT = "Reconciliation account"
    LOAN = "Loan"
    DEBT = "Debt"
    MORTGAGE = "Mortgage"
