from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# ---------- Auth ----------
class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    # bcrypt only uses the first 72 bytes of a password.
    password: str = Field(min_length=8, max_length=72)


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ---------- Groups ----------
class GroupCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)


class GroupOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    created_by_id: int
    members: list[UserOut]


class AddMember(BaseModel):
    email: EmailStr


# ---------- Expenses ----------
class ExpenseCreate(BaseModel):
    description: str = Field(min_length=1, max_length=200)
    amount: Decimal = Field(gt=0, max_digits=12, decimal_places=2, examples=["1500.00"])
    paid_by_id: int | None = Field(default=None, description="Defaults to the logged-in user")
    split_between: list[int] | None = Field(
        default=None, description="User ids to split equally between; defaults to all members"
    )


class ShareOut(BaseModel):
    user_id: int
    amount: Decimal


class ExpenseOut(BaseModel):
    id: int
    description: str
    amount: Decimal
    paid_by_id: int
    created_at: datetime
    shares: list[ShareOut]


# ---------- Balances ----------
class BalanceOut(BaseModel):
    user_id: int
    name: str
    balance: Decimal = Field(description="Positive: others owe this user. Negative: this user owes.")


class SettlementOut(BaseModel):
    from_user_id: int
    to_user_id: int
    amount: Decimal
