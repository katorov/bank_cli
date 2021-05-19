import datetime
from decimal import Decimal

from prettytable import PrettyTable, ALL

from datetime_utils import DatetimeRange, string_to_datetime, datetime_to_string


class Transaction:
    """Bank transaction"""

    def __init__(self, account, amount, description, is_deposit=False, is_withdraw=False):
        if amount <= 0:
            raise ValueError('amount must be positive')
        if not is_deposit and not is_withdraw:
            raise ValueError('is_deposit or is_withdraw must be True')

        self.account = account
        self.amount = amount
        self.description = description
        self.is_deposit = is_deposit
        self.is_withdraw = is_withdraw
        self.created_at = datetime.datetime.now()
        self.balance = self.get_balance()

    def get_balance(self):
        if self.is_deposit:
            return self.account.balance + self.amount
        return self.account.balance - self.amount


class Account:
    """Bank account"""
    all_accounts = dict()

    def __init__(self, client: str):
        self.client = client
        self.balance = Decimal('0.00')
        self.transactions = list()

    @classmethod
    def _get_or_create(cls, client: str):
        """Get or create Account"""
        try:
            account = cls.all_accounts[client]
        except KeyError:
            account = Account(client)
            cls.all_accounts[client] = account
        return account

    @classmethod
    def deposit(cls, client, amount, description) -> None:
        """Add deposit operation"""
        if amount <= 0:
            raise ValueError('Amount must be positive')
        account = cls._get_or_create(client)
        deposit_transaction = Transaction(account, amount, description, is_deposit=True)
        account.transactions.append(deposit_transaction)
        account.balance = deposit_transaction.balance

    @classmethod
    def withdraw(cls, client, amount, description) -> None:
        """Add withdrawal operation"""
        if amount <= 0:
            raise ValueError('Amount must be positive')
        account = cls._get_or_create(client)
        withdraw_transaction = Transaction(account, amount, description, is_withdraw=True)
        account.transactions.append(withdraw_transaction)
        account.balance = withdraw_transaction.balance

    def get_transactions(self, since: datetime.datetime = None, till: datetime.datetime = None):
        """Get sorted transactions for chosen dates"""
        all_transactions = self.transactions
        transactions = [t for t in all_transactions if t.created_at in DatetimeRange(since, till)]
        transactions.sort(key=lambda transaction: transaction.created_at)
        return transactions

    def get_balance(self, specified_dt: datetime.datetime = None) -> Decimal:
        """Get current balance or balance for chosen dates"""
        if not specified_dt:
            return self.balance

        try:
            return self.get_transactions(till=specified_dt)[-1].balance
        except IndexError:
            return Decimal('0.00')

    @classmethod
    def get_bank_statement_table(cls, client, since, till):
        """Get prettify account statement for chosen dates"""
        account = cls._get_or_create(client)
        since = string_to_datetime(since)
        till = string_to_datetime(till)
        transactions = account.get_transactions(since, till)
        previous_balance = account.get_balance(since).quantize(Decimal('0.00'))
        total_balance = account.get_balance(till).quantize(Decimal('0.00'))
        totals = dict(
            withdrawals=Decimal('0.00'),
            deposits=Decimal('0.00')
        )

        th = ['Date', 'Description', 'Withdrawals', 'Deposits', 'Balance']
        bank_statement_table = PrettyTable(th, hrules=ALL)
        bank_statement_table.add_row(
            ('', 'Previous balance', '', '', f"${previous_balance}")
        )

        for transaction in transactions:
            amount = transaction.amount.quantize(Decimal('0.00'))
            bank_statement_table.add_row(
                (
                    datetime_to_string(transaction.created_at),
                    transaction.description,
                    f"${amount}" if transaction.is_withdraw else '',
                    f"${amount}" if transaction.is_deposit else '',
                    f"${transaction.balance.quantize(Decimal('0.00'))}",
                )
            )
            if transaction.is_withdraw:
                totals['withdrawals'] += amount
            else:
                totals['deposits'] += amount

        bank_statement_table.add_row(
            ('',
             'Totals',
             f"${totals['withdrawals']}",
             f"${totals['deposits']}",
             f"${total_balance}")
        )

        return bank_statement_table
