from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class GroupMember(Base):
    """Join table: which users belong to which group."""

    __tablename__ = "group_members"

    group_id: Mapped[int] = mapped_column(
        ForeignKey("expense_groups.id", ondelete="CASCADE"), primary_key=True
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)


class Group(Base):
    # "groups" is a reserved word in MySQL 8, so the table gets a safer name.
    __tablename__ = "expense_groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    created_by_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    members: Mapped[list[User]] = relationship(secondary="group_members")
    expenses: Mapped[list["Expense"]] = relationship(
        back_populates="group", cascade="all, delete-orphan"
    )


class Expense(Base):
    __tablename__ = "expenses"

    id: Mapped[int] = mapped_column(primary_key=True)
    group_id: Mapped[int] = mapped_column(ForeignKey("expense_groups.id", ondelete="CASCADE"))
    paid_by_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    description: Mapped[str] = mapped_column(String(200))
    # Money is stored as whole paisa (Rs 150.50 -> 15050) to avoid float rounding errors.
    amount_paisa: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    group: Mapped[Group] = relationship(back_populates="expenses")
    shares: Mapped[list["ExpenseShare"]] = relationship(cascade="all, delete-orphan")


class ExpenseShare(Base):
    """How much of one expense a single user is responsible for."""

    __tablename__ = "expense_shares"

    expense_id: Mapped[int] = mapped_column(
        ForeignKey("expenses.id", ondelete="CASCADE"), primary_key=True
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    share_paisa: Mapped[int] = mapped_column(Integer)
