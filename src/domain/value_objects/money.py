from dataclasses import dataclass


@dataclass(frozen=True)
class Money:
    amount: int
    currency: str = "RUB"

    def __post_init__(self) -> None:
        if self.amount < 0:
            raise ValueError("Money amount cannot be negative")

    def __add__(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError(f"Currency mismatch: {self.currency} != {other.currency}")
        return Money(self.amount + other.amount, self.currency)

    def __sub__(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError(f"Currency mismatch: {self.currency} != {other.currency}")
        return Money(self.amount - other.amount, self.currency)

    def __lt__(self, other: "Money") -> bool:
        return self.amount < other.amount
