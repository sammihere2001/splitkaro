from fastapi import APIRouter, HTTPException, status

from app.deps import CurrentUser, DbSession, MemberGroup
from app.models import Expense, ExpenseShare
from app.money import to_paisa, to_rupees
from app.schemas import ExpenseCreate, ExpenseOut, ShareOut
from app.services.settlement import split_equally

router = APIRouter(prefix="/groups/{group_id}/expenses", tags=["expenses"])


def to_expense_out(expense: Expense) -> ExpenseOut:
    return ExpenseOut(
        id=expense.id,
        description=expense.description,
        amount=to_rupees(expense.amount_paisa),
        paid_by_id=expense.paid_by_id,
        created_at=expense.created_at,
        shares=[ShareOut(user_id=s.user_id, amount=to_rupees(s.share_paisa)) for s in expense.shares],
    )


@router.post("", response_model=ExpenseOut, status_code=status.HTTP_201_CREATED)
def add_expense(data: ExpenseCreate, group: MemberGroup, user: CurrentUser, db: DbSession):
    member_ids = [m.id for m in group.members]

    paid_by_id = data.paid_by_id if data.paid_by_id is not None else user.id
    if paid_by_id not in member_ids:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Payer must be a member of the group")

    split_between = data.split_between if data.split_between is not None else member_ids
    if not split_between:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "split_between cannot be empty")
    if len(set(split_between)) != len(split_between):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "split_between has duplicate users")
    if not set(split_between) <= set(member_ids):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Everyone in split_between must be a member")

    amount_paisa = to_paisa(data.amount)
    shares = split_equally(amount_paisa, split_between)

    expense = Expense(
        group_id=group.id,
        paid_by_id=paid_by_id,
        description=data.description,
        amount_paisa=amount_paisa,
        shares=[ExpenseShare(user_id=uid, share_paisa=share) for uid, share in shares.items()],
    )
    db.add(expense)
    db.commit()
    return to_expense_out(expense)


@router.get("", response_model=list[ExpenseOut])
def list_expenses(group: MemberGroup):
    newest_first = sorted(group.expenses, key=lambda e: (e.created_at, e.id), reverse=True)
    return [to_expense_out(e) for e in newest_first]


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(expense_id: int, group: MemberGroup, user: CurrentUser, db: DbSession):
    expense = db.get(Expense, expense_id)
    if expense is None or expense.group_id != group.id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Expense not found")
    if user.id not in (expense.paid_by_id, group.created_by_id):
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, "Only the payer or the group creator can delete this"
        )

    db.delete(expense)
    db.commit()
