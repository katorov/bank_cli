import decimal
from decimal import Decimal

import click
from click_shell import shell

from services import Account


@shell(prompt='bank > ', intro='Service started!')
def main():
    """Service that simulates the bank's work with customer accounts"""
    decimal_context = decimal.Context(rounding=decimal.ROUND_HALF_DOWN)
    decimal.setcontext(decimal_context)


@main.command()
@click.option("--client", help="Full name", type=str, required=True)
@click.option("--amount", help="Amount, $", type=Decimal, required=True)
@click.option("--description", help="Description", type=str, required=True)
def deposit(client, amount, description):
    """Add deposit operation"""
    Account.deposit(client, amount, description)
    click.echo('Deposit operation was successful!')


@main.command()
@click.option("--client", help="Full name", type=str, required=True)
@click.option("--amount", help="Amount, $", type=Decimal, required=True)
@click.option("--description", help="Description", type=str, required=True)
def withdraw(client, amount, description):
    """Add withdrawal operation"""
    Account.withdraw(client, amount, description)
    click.echo('Withdrawal operation was successful!')


@main.command(name='show_bank_statement')
@click.option("--client", help="Full name", type=str, required=True)
@click.option("--since", help="Datetime (example: 2021-01-01 00:00:00)", type=str, required=True)
@click.option("--till", help="Datetime (example: 2021-01-01 00:00:00)", type=str, required=True)
def show_bank_statement(client, since=1, till=1):
    """Show transactions for chosen dates"""
    table = Account.get_bank_statement_table(client, since, till)
    click.echo(table)


if __name__ == "__main__":
    main()
