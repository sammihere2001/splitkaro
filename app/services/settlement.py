"""The money logic of SplitKaro.

Everything in here works in paisa (integers), never floats: 0.1 + 0.2 != 0.3 in floating point,
and you don't want someone to owe Rs 333.33333.
"""

from collections import defaultdict
from collections.abc import Iterable

from app.models import Expense


def split_equally(amount_paisa: int, user_ids: list[int]) -> dict[int, int]:
    
    """Splits an amount equally; leftover paisa go one each to the first users.

    Rs 100 between 3 people -> 3334, 3333, 3333 paisa (adds up to exactly 10000).
    """
    base, remainder = divmod(amount_paisa, len(user_ids))
    return {user_id: base + (1 if i < remainder else 0) for i, user_id in enumerate(user_ids)}


def compute_balances(expenses: Iterable[Expense]) -> dict[int, int]:
    """Net balance per user id.

    Positive -> the group owes this user money. Negative -> this user owes the group.
    All balances always add up to 0.
    """
    balances: dict[int, int] = defaultdict(int)
    for expense in expenses:
        balances[expense.paid_by_id] += expense.amount_paisa
        for share in expense.shares:
            balances[share.user_id] -= share.share_paisa
    return dict(balances)


def settle_up(balances: dict[int, int]) -> list[tuple[int, int, int]]:
    
    debtors = []    # people who owe:      (user_id, how_much_they_owe)
    creditors = []  # people who are owed: (user_id, how_much_they_are_owed)

    for user_id, balance in balances.items():
        if balance < 0:
            debtors.append((user_id, -balance))      
        elif balance > 0:                     
            creditors.append((user_id, balance))   

    payments = []

    while debtors and creditors:              # both lists still have people
        debtor_id, owes = debtors[0]          # first person who owes
        creditor_id, owed = creditors[0]      # first person who is owed

        amount = min(owes, owed)              

        payments.append((debtor_id, creditor_id, amount))   

        owes = owes - amount
        owed = owed - amount

        # update or remove the debtor
        if owes == 0:
            debtors.pop(0)                    # fully paid, so remove them
        else:
            debtors[0] = (debtor_id, owes)    # still owes something

        # do the same for the creditor
        if owed == 0:                       
            creditors.pop(0)
        else:
            creditors[0] = (creditor_id, owed)        

    return payments