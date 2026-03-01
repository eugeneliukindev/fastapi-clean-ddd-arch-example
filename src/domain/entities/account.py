from dataclasses import dataclass
from enum import StrEnum
from uuid import uuid4

from src.domain.entities.base import BaseEntity
from src.domain.exceptions import AccountFrozenException, ConflictException, InsufficientFundsException
from src.domain.value_objects.money import Money


class AccountStatus(StrEnum):
    ACTIVE = "active"
    FROZEN = "frozen"


@dataclass
class Account(BaseEntity):
    owner: str
    balance: Money
    status: AccountStatus

    def __post_init__(self) -> None:
        if len(self.owner) > 100:
            raise ValueError("Owner cannot exceed 100 characters")

    @classmethod
    def new(cls, owner: str, balance: Money) -> "Account":
        return cls(id=uuid4(), owner=owner, balance=balance, status=AccountStatus.ACTIVE)

    def deposit(self, amount: Money) -> None:
        if self.status == AccountStatus.FROZEN:
            raise AccountFrozenException(f"Account {self.id} is frozen")
        if amount.amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.balance = self.balance + amount

    def withdraw(self, amount: Money) -> None:
        if self.status == AccountStatus.FROZEN:
            raise AccountFrozenException(f"Account {self.id} is frozen")
        if amount.amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if self.balance < amount:
            raise InsufficientFundsException(
                f"Insufficient funds: balance {self.balance.amount}, requested {amount.amount}"
            )
        self.balance = self.balance - amount

    def freeze(self) -> None:
        if self.status == AccountStatus.FROZEN:
            raise ConflictException(f"Account {self.id} is already frozen")
        self.status = AccountStatus.FROZEN

    def unfreeze(self) -> None:
        if self.status == AccountStatus.ACTIVE:
            raise ConflictException(f"Account {self.id} is already active")
        self.status = AccountStatus.ACTIVE
