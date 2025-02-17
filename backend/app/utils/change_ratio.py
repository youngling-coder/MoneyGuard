from datetime import datetime
from decimal import Decimal

from .. import models


def get_change_ratio(compared: Decimal, reference: Decimal) -> Decimal:

    change_ratio = Decimal("100.0")

    if reference:
        change_ratio = (compared - reference) / reference * change_ratio

        return change_ratio

    else:
        return change_ratio


def get_balance_change_ratio(
    total_balance: Decimal,
    month: int,
    transactions: list[models.Transaction],
    change_ratio: Decimal = Decimal("100.00"),
    precision: int = 2,
):

    current_date = datetime.now()
    current_year = target_year = current_date.year
    target_month = month

    if current_date.month < target_month:
        target_year = current_year - 1

    from_date = datetime(target_year, target_month, 1)

    if target_month == 1:
        target_month = 12
        target_year -= 1

    else:
        target_month -= 1

    prev_from_date = datetime(target_year, target_month, 1)

    to_date = datetime.now()

    selected_month_transactions = list(
        filter(lambda t: from_date <= t.timestamp <= to_date, transactions)
    )
    previous_month_transactions = list(
        filter(lambda t: prev_from_date <= t.timestamp <= to_date, transactions)
    )

    previous_month_balance = selected_month_balance = total_balance

    for transaction in selected_month_transactions:
        selected_month_balance -= transaction.amount

    for transaction in previous_month_transactions:
        previous_month_balance -= transaction.amount

    change_ratio = round(
        float(
            get_change_ratio(
                compared=selected_month_balance, reference=previous_month_balance
            )
        ),
        ndigits=precision,
    )

    if (selected_month_balance < previous_month_balance and change_ratio > 0) or (
        selected_month_balance > previous_month_balance and change_ratio < 0
    ):
        change_ratio = -change_ratio

    return selected_month_balance, change_ratio


def get_transactions_change_ratio(
    month: int,
    transactions: list,
    change_ratio: Decimal = Decimal("100.0"),
    precision: int = 2,
):

    current_date = datetime.now()
    current_year = target_year = current_date.year
    target_month = month

    if current_date.month < target_month:
        target_year = current_year - 1

    selected_month_transactions = list(
        filter(
            lambda t: t.timestamp.year == target_year
            and t.timestamp.month == target_month,
            transactions,
        )
    )

    if target_month == 1:
        target_year = current_year - 1
        target_month = 12
    else:
        target_month -= 1

    previous_month_transactions = list(
        filter(
            lambda t: t.timestamp.year == target_year
            and t.timestamp.month == target_month,
            transactions,
        )
    )

    current_amount = 0
    previous_amount = 0

    current_amount = sum(map(lambda t: t.amount, selected_month_transactions))
    previous_amount = sum(map(lambda t: t.amount, previous_month_transactions))

    change_ratio = round(
        float(get_change_ratio(compared=previous_amount, reference=previous_amount)),
        ndigits=precision,
    )

    return current_amount, change_ratio
