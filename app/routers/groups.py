from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from app.deps import CurrentUser, DbSession, MemberGroup
from app.models import Group, GroupMember, User
from app.money import to_rupees
from app.schemas import AddMember, BalanceOut, GroupCreate, GroupOut, SettlementOut
from app.services.settlement import compute_balances, settle_up

router = APIRouter(prefix="/groups", tags=["groups"])


@router.post("", response_model=GroupOut, status_code=status.HTTP_201_CREATED)
def create_group(data: GroupCreate, user: CurrentUser, db: DbSession):
    group = Group(name=data.name, created_by_id=user.id, members=[user])
    db.add(group)
    db.commit()
    return group


@router.get("", response_model=list[GroupOut])
def list_my_groups(user: CurrentUser, db: DbSession):
    query = (
        select(Group)
        .join(GroupMember, GroupMember.group_id == Group.id)
        .where(GroupMember.user_id == user.id)
        .order_by(Group.created_at.desc())
    )
    return db.scalars(query).all()


@router.get("/{group_id}", response_model=GroupOut)
def get_group(group: MemberGroup):
    return group


@router.post("/{group_id}/members", response_model=GroupOut)
def add_member(data: AddMember, group: MemberGroup, db: DbSession):
    new_member = db.scalar(select(User).where(User.email == data.email.lower()))
    if new_member is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No user registered with that email")
    if new_member in group.members:
        raise HTTPException(status.HTTP_409_CONFLICT, "User is already in this group")

    group.members.append(new_member)
    db.commit()
    return group


@router.get("/{group_id}/balances", response_model=list[BalanceOut])
def get_balances(group: MemberGroup):
    balances = compute_balances(group.expenses)
    return [
        BalanceOut(user_id=m.id, name=m.name, balance=to_rupees(balances.get(m.id, 0)))
        for m in group.members
    ]


@router.get("/{group_id}/settle-up", response_model=list[SettlementOut])
def get_settle_up(group: MemberGroup):
    """A short list of payments (at most one fewer than the people involved) that evens everyone out."""
    payments = settle_up(compute_balances(group.expenses))
    return [
        SettlementOut(from_user_id=payer, to_user_id=receiver, amount=to_rupees(amount))
        for payer, receiver, amount in payments
    ]
