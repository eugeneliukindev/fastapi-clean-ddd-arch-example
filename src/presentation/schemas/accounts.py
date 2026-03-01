from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from src.domain.entities.account import AccountStatus


class AccountCreate(BaseModel):
    owner: str = Field(min_length=1, max_length=100)
    initial_balance: int = Field(default=0, ge=0)
    currency: str = Field(default="RUB", min_length=3, max_length=3)


class MoneyRequest(BaseModel):
    amount: int = Field(gt=0)
    currency: str = Field(default="RUB", min_length=3, max_length=3)


class MoneyResponse(BaseModel):
    amount: int
    currency: str


class AccountResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    owner: str
    balance: MoneyResponse
    status: AccountStatus
