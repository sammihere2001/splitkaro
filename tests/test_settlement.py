import pytest

from app.models import Expense, ExpenseShare
from app.services.settlement import compute_balances, settle_up, split_equally


# ---------- split_equally & compute_balances (already implemented) ----------
def test_split_equally_adds_up_exactly():
    shares = split_equally(10000, [1, 2, 3])
    assert shares == {1: 3334, 2: 3333, 3: 3333}
    assert sum(shares.values()) == 10000


def test_compute_balances():
    expenses = [
        Expense(paid_by_id=1, amount_paisa=3000,
                shares=[ExpenseShare(user_id=u, share_paisa=1000) for u in (1, 2, 3)]),
        Expense(paid_by_id=2, amount_paisa=600,
                shares=[ExpenseShare(user_id=u, share_paisa=300) for u in (2, 3)]),
    ]
    assert compute_balances(expenses) == {1: 2000, 2: -700, 3: -1300}


# ---------- settle_up (your task!) ----------
def assert_settles(balances: dict[int, int], payments: list[tuple[int, int, int]]):
    """Checks every rule from the settle_up docstring."""
    remaining = dict(balances)
    for payer, receiver, amount in payments:
        assert amount > 0, f"payment amounts must be positive, got {amount}"
        assert payer != receiver, "nobody should pay themselves"
        remaining[payer] += amount
        remaining[receiver] -= amount
    assert all(b == 0 for b in remaining.values()), f"not settled, left over: {remaining}"

    people_involved = sum(1 for b in balances.values() if b != 0)
    assert len(payments) <= max(people_involved - 1, 0), "too many payments"


def test_nothing_to_settle():
    assert settle_up({}) == []
    assert settle_up({1: 0, 2: 0}) == []


def test_two_people():
    assert settle_up({1: 500, 2: -500}) == [(2, 1, 500)]


def test_one_person_paid_for_everyone():
    balances = {1: 2000, 2: -1000, 3: -1000}
    payments = settle_up(balances)
    assert_settles(balances, payments)
    assert sorted(payments) == [(2, 1, 1000), (3, 1, 1000)]


def test_person_with_zero_balance_is_not_involved():
    payments = settle_up({1: -1000, 2: 0, 3: 1000})
    assert payments == [(1, 3, 1000)]


@pytest.mark.parametrize(
    "balances",
    [
        {1: 2000, 2: -700, 3: -1300},
        {1: 5000, 2: 3000, 3: -2500, 4: -2500, 5: -3000},
        {1: 1, 2: 1, 3: -2},
        {1: 3334, 2: -3333, 3: -1},
        {i: (i * 37) % 101 - 50 for i in range(1, 10)} | {10: -sum((i * 37) % 101 - 50 for i in range(1, 10))},
    ],
)
def test_settles_everyone(balances):
    assert sum(balances.values()) == 0  # sanity check on the test data itself
    assert_settles(balances, settle_up(balances))


def test_does_not_modify_input():
    balances = {1: 2000, 2: -700, 3: -1300}
    settle_up(balances)
    assert balances == {1: 2000, 2: -700, 3: -1300}
